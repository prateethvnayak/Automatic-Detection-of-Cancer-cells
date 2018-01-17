import os
import glob
import cv2
import matplotlib
import skimage

import benchmark
import seg_main_WoD
# from core.algo.reference import segment
import ground_truth
import scipy.ndimage as nd
""" Use below imports for making file list and writing into excel sheet 
import list_files as lf
from xlrd import open_workbook
from xlutils.copy import copy
"""


def segment(path, num):

    matplotlib.use('Qt5Agg')
    bgr_image = cv2.imread(path)
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    (row, col, d) = bgr_image.shape
    if num == 1:                                # for kidwai dataset
        xml_file = path[:-3] + 'xml'
        gt = ground_truth.xml2mask(xml_file, (row, col))
    else :                                      # for herlev dataset
        bmp_file = path[:-4] + '-d.bmp'
        gt = ground_truth.bmp2mask(bmp_file)

    # # "Delete contents of cropped directory"
    # directory = "/home/intern/PycharmProjects/tf_files/Cropped"
    # """ os.chdir(directory)
    # files = glob.glob('*.jpeg')
    # for filename in files:
    #     os.unlink(filename)
    # """

    # seed region
    est = seg_main_WoD.main(nd.imread(path), nd.imread(path, flatten=True), num)  # segments the nuclei using technique

    # # find the labels and number of segments after segmentation
    # lbel, n = skimage.measure.label(est, return_num=True)
    #
    # if n > 1:           # if multiple nuclei segmented
    #     p_list = skimage.measure.regionprops(lbel)  # Using regionprops to get properties of segments
    #
    #     for i in range(0, n):
    #         if p_list[i].area > 750:
    #             [minr, minc, maxr, maxc] = p_list[i].bbox
    #             as_ratio = float(maxr)/maxc
    #             if as_ratio > 0.40:
    #                 cropped = bgr_image[minr:maxr, minc:maxc]
    #                 cv2.imwrite(directory+'/kidwai_crop/'+ path[-8:-4]+'cropped'+str(i)+'.jpeg',cropped)
    #
    # else:               # if single nuclei segmented
    #     p_list = skimage.measure.regionprops(lbel)
    #     [minr, minc, maxr, maxc] = p_list[0].bbox
    #     cropped = bgr_image[minr:maxr, minc:maxc]
    #     cv2.imwrite(directory+'/herlev_crop/'+path[-8:-4]+'cropped.jpeg', cropped)

    # Finding the precision and recall with the Annotated data (ground truth mask)
    precision, recall = benchmark.perfomance_measure(gt, est)
    precision = round(precision, 6)
    recall = round(recall, 6)

    status = benchmark.measure_seed_region(gt, est)     # gives the status of segments
    print status

    return precision, recall



""" Writing the results into Excel sheet
rb = open_workbook(
    "/home/intern/PycharmProjects/kidwai_normal.xls")  # Location of excel worksheet(with name and extension)
wb = copy(rb)
s = wb.get_sheet(0)
s.write(r, 0, img[i])
s.write(r, 1, status['total_estimated_nucleus'])
s.write(r, 2, status['total_gt_nucleus'])
s.write(r, 3, status['missed_nucleus'])
s.write(r, 4, status['incorrect_nucleus'])
s.write(r, 5, status['single_nucleus'])
s.write(r, 6, status['multiple_nucleus'])
s.write(r, 7, precision)
s.write(r, 8, recall)

wb.save("/home/intern/PycharmProjects/kidwai_normal.xls")  # Location of excel worksheet(with name and extension)

"""
