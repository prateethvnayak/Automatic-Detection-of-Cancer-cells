import os
import glob
import seg_main_d
from skimage import measure as sm
import matplotlib
import scipy.ndimage as nd
import cv2


def main_call(path, num):
    matplotlib.use('Qt5Agg')
    bgr_image = cv2.imread(path)
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

    # seed region
    est = seg_main_d.main(nd.imread(path), nd.imread(path, flatten=True), num)  # segments the nuclei using technique

    # "Delete contents of cropped directory"
    import shutil
    directory = "ROOT DIRECTORY NAME/cropped"   # GIVE PATH TO SAVE CROP FILES (inside which two folders - kidwai_crop & herlev_crop need to be present)
    if num == 1:
        if os.path.exists(directory+'/kidwai_crop'):
            shutil.rmtree(directory + '/kidwai_crop')

    else:
        if os.path.exists(directory + '/herlev_crop'):
            shutil.rmtree(directory + '/herlev_crop')

    # find the labels and number of segments after segmentation
    lbel, n = sm.label(est, return_num=True)
    newpath = r"ROOT DIRECORY NAME/cropped"
    p_list = sm.regionprops(lbel)  # Using regionprops to get properties of segments
    if num == 1:    # for kidwai set
        os.makedirs(newpath+'/kidwai_crop')
        for i in range(0, n):
            if p_list[i].area > 750:
                [minr, minc, maxr, maxc] = p_list[i].bbox
                as_ratio = float(maxr) / maxc
                if as_ratio > 0.40:
                    cropped = bgr_image[minr:maxr, minc:maxc]
                    cv2.imwrite(directory + '/kidwai_crop/' + path[-8:-4] + 'cropped' + str(i) + '.jpeg', cropped)
    else:      # for Herlev Set
        os.makedirs(newpath+'/herlev_crop')
        for i in range (0, n):
            if p_list[i].area>1000:
                [minr, minc, maxr, maxc] = p_list[i].bbox
                cropped = bgr_image[minr:maxr, minc:maxc]
                cv2.imwrite(directory + '/herlev_crop/' + path[-8:-4] + 'cropped'+str(i)+'.jpeg', cropped)
