# ----------------------------------------------------------------------------------------------------------------------
# Localizing Region-Based Active Contours
#
# seg = region_seg(I, init_mask, max_its, alpha, display)
#
# Inputs: I           2D image
#         smask       Initialization (1 = foreground, 0 = bg) (seed region)
#         max_its     Number of iterations to run segmentation for
#         alpha       (optional) Weight of smoothing term
#                       higher = smoother.  default = 0.2
#         display     (optional) displays intermediate outputs
#                       default = true
#
# Outputs: output        Final segmentation mask (1=fg, 0=bg)
#
# Description: This code implements the Localizing Region-Based Active Contours
#              which is capable of segmenting objects with heterogeneous feature
#              profiles that would be difficult to capture correctly using a standard global method.
#
# Author - Aindra Systems Pvt. Ltd.
# ----------------------------------------------------------------------------------------------------------------------
import cv2
import numpy as np
import scipy
import scipy.ndimage as nd
import matplotlib.pyplot as plt
import seedregion as sd

eps = np.finfo(float).eps     # small value


def chanvese(I, init_mask, max_its, thresh=-1, color='r', display=False):
    I = I.astype(np.float)
    # Create a signed distance function (SDF) from mask
    phi = mask2phi(init_mask)

    if display:
        plt.ion()
        fig, axes = plt.subplots(ncols=2)
        show_curve_and_phi(fig, I, phi, color)
        # plt.savefig('C:\Users\User\PycharmProjects\ACD\levelset_start.png', bbox_inches='tight')

    # Main loop
    its = 0
    stop = False
    prev_mask = init_mask
    c = 0

    while its < max_its and not stop:
        idx = np.flatnonzero(np.logical_and(phi <= 1.2, phi >= -1.2))
        phi0 = heaviside(phi)

        if len(idx) > 0:
            # Intermediate output
            if display:
                if np.mod(its, 5) == 0:
                    print('iteration: {0}'.format(its))
                    show_curve_and_phi(fig, I, phi, color)
            else:
                if np.mod(its, 10) == 0:
                    print('iteration: {0}'.format(its))

            # computing mean intensities using uniform modelling
            Au = np.sum(cv2.blur(phi0, (3, 3)))
            Av = np.sum(cv2.blur((1-phi0), (3, 3)))

            ux = np.sum(cv2.blur((phi0*I), (3, 3))) / Au   # interior
            vx = np.sum(cv2.blur((1-phi0)*I, (3, 3))) / Av  # exterior

            # applying level set formulae
            a = (I - ux)**2
            b = (I - vx)**2
            c1 = (a - b)

            # Gradient descent to minimize energy
            dphidt = dirac(phi) * (cv2.blur(c1, (3, 3)))

            # normalizing gradient
            dphidt /= (np.max(np.abs(dphidt)))

            # Maintain the CFL condition
            dt = 0.40 / (np.max(np.abs(dphidt)) + eps)

            # Evolve the curve
            phi += (dt * dphidt)

            # Keep SDF smooth
            phi = sussman(phi, 0.5)

            new_mask = phi <= 0
            c = convergence(prev_mask, new_mask, thresh, c)

            if c <= 3:
                its += 1
                prev_mask = new_mask
            else:
                stop = True

        else:
            break

    # Final output
    if display:
        show_curve_and_phi(fig, I, phi, color)
        # plt.savefig('C:\Users\User\PycharmProjects\ACD\levelset_end.png', bbox_inches='tight')

    # Make mask from SDF
    seg = phi <= 0  # Get mask from levelset

    return seg, phi, its


# ---------------------------------------------------------------------
# ---------------------- AUXILIARY FUNCTIONS --------------------------
# ---------------------------------------------------------------------

def bwdist(a):
    """
    Intermediary function. 'a' has only True/False vals,
    so we convert them into 0/1 values - in reverse.
    True is 0, False is 1, distance_transform_edt wants it that way.
    """
    return nd.distance_transform_edt(a == 0)


# Displays the image with curve superimposed
def show_curve_and_phi(fig, I, phi, color):
    fig.axes[0].cla()
    fig.axes[0].imshow(I, cmap='gray')
    fig.axes[0].contour(phi, 0, colors=color)
    fig.axes[0].set_axis_off()
    plt.draw()

    fig.axes[1].cla()
    fig.axes[1].imshow(phi)
    fig.axes[1].set_axis_off()
    plt.draw()

    plt.pause(0.001)


def im2double(a):
    a = a.astype(np.float)
    a /= np.abs(a).max() + eps
    return a


# Converts a mask to a SDF
def mask2phi(init_a):
    phi = bwdist(init_a) - bwdist(1 - init_a) + im2double(init_a) - 0.5
    return phi




# Level set re-initialization by the Sussman method
def sussman(D, dt):
    # forward/backward differences
    a = D - np.roll(D, 1, axis=1)
    b = np.roll(D, -1, axis=1) - D
    c = D - np.roll(D, -1, axis=0)
    d = np.roll(D, 1, axis=0) - D

    a_p = np.clip(a, 0, np.inf)
    a_n = np.clip(a, -np.inf, 0)
    b_p = np.clip(b, 0, np.inf)
    b_n = np.clip(b, -np.inf, 0)
    c_p = np.clip(c, 0, np.inf)
    c_n = np.clip(c, -np.inf, 0)
    d_p = np.clip(d, 0, np.inf)
    d_n = np.clip(d, -np.inf, 0)

    a_p[a < 0] = 0
    a_n[a > 0] = 0
    b_p[b < 0] = 0
    b_n[b > 0] = 0
    c_p[c < 0] = 0
    c_n[c > 0] = 0
    d_p[d < 0] = 0
    d_n[d > 0] = 0

    dD = np.zeros_like(D)
    D_neg_ind = np.flatnonzero(D < 0)
    D_pos_ind = np.flatnonzero(D > 0)

    dD.flat[D_pos_ind] = np.sqrt(
        np.max(np.concatenate(
            ([a_p.flat[D_pos_ind] ** 2], [b_n.flat[D_pos_ind] ** 2])), axis=0) +
        np.max(np.concatenate(
            ([c_p.flat[D_pos_ind] ** 2], [d_n.flat[D_pos_ind] ** 2])), axis=0)) - 1
    dD.flat[D_neg_ind] = np.sqrt(
        np.max(np.concatenate(
            ([a_n.flat[D_neg_ind] ** 2], [b_p.flat[D_neg_ind] ** 2])), axis=0) +
        np.max(np.concatenate(
            ([c_n.flat[D_neg_ind] ** 2], [d_p.flat[D_neg_ind] ** 2])), axis=0)) - 1

    D -= dt * sussman_sign(D) * dD
    return D


def sussman_sign(D):
    return D / np.sqrt(D ** 2 + 1)


# Convergence Test
def convergence(p_mask, n_mask, thresh, c):
    diff = p_mask - n_mask
    n_diff = np.sum(np.abs(diff))
    if n_diff < thresh:
        c += 1
    else:
        c = 0
    return c


# Heaviside Function
def heaviside(p):
    [i, j] = np.shape(p)
    out = np.zeros(p.shape)
    for m in range(0, i-1, 1):
        for n in range(0, j-1, 1):
            if p[m, n] < -eps:
                out[m, n] = 1
            elif p[m, n] > eps:
                out[m, n] = 0
            else:
                out[m, n] = (1 + (p[m, n]/eps) + (1/3.14) * np.math.sin(3.14 * p[m, n] / eps))/2

    return out


# Dirac function
def dirac(p):
    out = np.abs(p) <= 0.5

    return out


def scale(image, scaling_factor):
    [i, j] = np.shape(image)
    dif = np.zeros([i,j])
    mean = (np.amin(image) + np.amax(image)) / 2
    for m in range(0, i-1, 1):
        for n in range(0, j-1, 1):
            dif[m, n] = (image[m, n] - mean) * scaling_factor
            image[m, n] = dif[m, n] + mean
    return image


# Main function call
def main(pic, gray, n):

    mask = sd.get_seed_region_clustering_morphology(pic, n)
    smask = sd.seed_refinement(mask, pic)
    gray = scale(gray, 2)

    output, _, _ = chanvese(gray, smask, max_its=150, display=True)
    output = output.astype(int)

    return output

