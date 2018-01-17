import numpy as np
import cv2
from chanvese import chanvese
from sklearn.cluster import KMeans
from skimage.segmentation import slic
from skimage.filters import threshold_otsu, rank
from skimage.morphology import disk
from skimage.segmentation import mark_boundaries
import mahotas
from skimage import feature
import matplotlib.pyplot as plt




def get_seed_region_clustering_morphology(oiginal_color_image, n):
    original_gray_image = cv2.cvtColor(oiginal_color_image, cv2.COLOR_RGB2GRAY)  # convert to gray
    clean_image = cv2.medianBlur(original_gray_image, 5)        # blurring effect
    clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(3, 3))     # apply clahe (histogram equalization)
    image = clahe.apply(clean_image)
    (row, col) = image.shape
    normalized_image = np.divide(np.double(image), 255)     # normalizing
    feature = np.reshape(normalized_image, (-1, 1))
    dark = np.min(feature)
    if n == 1:
        nucleus_location = np.where(feature < 0.08)  # for kidwai dataset
    else:
        nucleus_location = np.where(feature < 0.17)  # for herlev dataset
    initial_segment = np.zeros((row * col, 1), dtype=np.uint8)
    initial_segment[nucleus_location] = 1
    output = np.reshape(initial_segment, (row, col))
    dilation = output
    dilation[np.where(dilation > 0)] = 255
    return dilation     # return the seed regions



def seed_refinement(mask, bgr_image):
    # Apply one round original chanvese to refine the seed region and reach saturation
    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    mask[mask == 255] = 1.0
    refined_mask, _, _ = chanvese(gray_image.astype(float), mask.astype(float), max_its=100, display=False, alpha=1.0)
    refined_mask[refined_mask > 0] = 255
    return refined_mask



#Meanshift

"""
def get_seed_region_using_superpixel(oiginal_color_image):
    segments = slic(oiginal_color_image, n_segments=1000, sigma=2)
    lbl = np.unique(segments)
    original_gray_image = cv2.cvtColor(oiginal_color_image, cv2.COLOR_RGB2GRAY)
    clean_image = cv2.medianBlur(original_gray_image, 1)
    clahe = cv2.createCLAHE(clipLimit=7.0, tileGridSize=(8, 8))
    image = clahe.apply(clean_image)
    (row, col) = image.shape
    output = np.zeros((row, col), dtype=np.uint8)
    normalized_image = np.divide(np.double(image), 255)
    for i in lbl:
        val = np.median(normalized_image[np.where(segments == i)])
        pixel_values = normalized_image[np.where(segments == i)]
        if val < 0.5:
            output[np.where(segments == i)] = 255
            # var = np.var(normalized_image[np.where(segments == i)])
        # else:
        #     dark_pixels = sum(pixel_values < 0.25)
        #     ratio1 = float(dark_pixels)/float(len(pixel_values))
        #     if ratio1 > 0.20:
        #         output[np.where(segments == i)] = 255

    return output
"""
"""
#kMeans
def do_kmeans_clustering(color_feature, clusters):
    kmeans = KMeans(clusters).fit(color_feature)
    labels = kmeans.predict(color_feature)
    return (labels, kmeans)


def find_nucleus_region(cluster_centers, labels, no_clusters):
    temp = []
    for i in range(no_clusters):
        temp.append(np.linalg.norm(cluster_centers[i]))

    NUCLEUS_FLAG = np.argmin(temp)
    return NUCLEUS_FLAG


def get_seed_region_two_step_process(feature, image):
    (row, col, depth) = image.shape
    (labels, kmeans) = do_kmeans_clustering(feature, 2)
    NUCLEUS_FLAG = find_nucleus_region(kmeans.cluster_centers_, labels, 2)
    first_level_nucleus_location = np.where(labels == NUCLEUS_FLAG)
    first_level_nucleus_color_feature = feature[first_level_nucleus_location[0], :]

    (labels2, kmeans2) = do_kmeans_clustering(first_level_nucleus_color_feature, 2)
    NUCLEUS_FLAG = find_nucleus_region(kmeans.cluster_centers_, labels, 2)
    second_level_nucleus_location = np.where(labels2 == NUCLEUS_FLAG)
    loc2 = second_level_nucleus_location[0]
    loc1 = first_level_nucleus_location[0]
    segmented_nucleus_location = loc1[loc2]

    final_segment = np.zeros((row * col, 1), dtype=np.uint8)
    final_segment[segmented_nucleus_location] = 1
    output = np.reshape(final_segment, (row, col))
    return output
"""