import mahotas as mh
import math
import numpy as np
import collections
from skimage.measure import regionprops
import matplotlib.pyplot as plt


def measure_seed_region(gt_mask, estimated_seed_mask):
    """

    :param gt_mask: ground truth mask
    :param estimated_seed_mask: seed mask generated using any algorithm
    :return: status regarding the number of correct/incorrectly detected nucleus
    """
    gt_label, gt_num_labels = mh.label(gt_mask)
    est_label, est_num_label = mh.label(estimated_seed_mask)
    gt_mask_vec = np.reshape(gt_label, (-1, 1))
    est_mask_vec = np.reshape(est_label, (-1, 1))
    status = {'total_gt_nucleus': gt_num_labels,
              'total_estimated_nucleus': est_num_label,
              'incorrect_nucleus': 0,
              'single_nucleus': 0,
              'multiple_nucleus': 0,
              'missed_nucleus': 0}
    for el in range(1, est_num_label, 1):
        est_loc = np.where(est_mask_vec == el)
        gt_label_at_loc = gt_mask_vec[est_loc]
        unique_gt_labels = np.unique(gt_label_at_loc)
        if len(unique_gt_labels) == 1 and 0 in unique_gt_labels:
            status['incorrect_nucleus'] += 1
        elif len(unique_gt_labels) == 2 and 0 in unique_gt_labels:
            status['single_nucleus'] += 1
        else:
            status['multiple_nucleus'] += 1

    for gl in range(1, gt_num_labels, 1):
        gt_loc = np.where(gt_mask_vec == gl)
        est_label_at_loc = est_mask_vec[gt_loc]
        unique_est_labels = np.unique(est_label_at_loc)
        if len(unique_est_labels) == 1 and unique_est_labels[0] is not 0:
            status['missed_nucleus'] += 1

    return status


def perfomance_measure(gt_mask, estimated_seed_mask):
    """

    :param gt_mask: ground truth mask
    :param estimated_seed_mask: seed mask generated using any algorithm
    :return: precision and recall values
    """
    est = estimated_seed_mask.reshape(-1,)
    detected_nucleus = collections.Counter(est)
    gt = gt_mask.reshape(-1,)
    groundtruth_nucleus = collections.Counter(gt)
    total_nucleus_pixels = groundtruth_nucleus[50]+groundtruth_nucleus[100]+groundtruth_nucleus[150]+\
                           groundtruth_nucleus[200]+groundtruth_nucleus[1]
    correctly_segmented = float(np.sum(np.logical_and(est > 0, gt > 0)))
    Precision = correctly_segmented/float(detected_nucleus[1])
    Recall = correctly_segmented/float(total_nucleus_pixels)

    est_labeled, est_nr_objects = mh.label(estimated_seed_mask)
    gt_labeled, gt_nr_objects = mh.label(gt_mask)

    property_list = regionprops(gt_labeled)
    for region in property_list:
        area = region.area
        perimeter = region.perimeter
        major_axis_length = region.major_axis_length
        minor_axis_length = region.minor_axis_length
        roundness = ((float(major_axis_length)/2)**2 * math.pi)/area
        solidity = region.solidity
        elongation = minor_axis_length/major_axis_length
        euler_number = region.euler_number
        print '_________________________________'
        print 'solidity', solidity
        print 'euler_number', euler_number
        print 'roundness', roundness
        print 'area', area
        print 'perimeter', perimeter
        print 'major_axis_length', major_axis_length
        print 'minor_axis_length', minor_axis_length
        print 'elongation', elongation
        print 'precision', Precision
        print '_________________________________'
        # bbox = region.bbox
        # temp = estimated_seed_mask[bbox[0]:bbox[2], bbox[1]:bbox[3]]
        # plt.imshow(temp)
        # plt.show()
        return Precision, Recall





