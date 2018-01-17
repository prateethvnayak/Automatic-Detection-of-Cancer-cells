from skimage import draw
import numpy as np
import xmltodict
import re
import cv2
import matplotlib.pyplot as plt

def number_of_cells(xml_file):
    """

    :param xml_file:
    :param shape:
    :return:
    """
    count = {'LSIL_Nucleus': 0,
             'HSIL_Nucleus': 0,
             'SCC_Nucleus': 0,
             'Nucleus_intermediate': 0,
             'Nucleus_superficial': 0,
             'Nucleus_parabasal': 0,
             'Nucleus_metaplasia': 0,
             'Nucleus_hystiocyte': 0,
             'Neutrophil': 0
             }
    with open(xml_file) as fd:
        doc = xmltodict.parse(fd.read())
    d_item = doc['root']
    for i in d_item:
        if re.match('rois', i) is not None:
            roi_item = d_item[i]
            for j in roi_item:
                if re.match('roi', j) is not None:
                    roi = roi_item[j]
                    for l in range(len(roi)):
                        class_name = roi[l]['classname']
                        name = str(roi[l]['name'])
                        if name in count.keys():
                            count[name] += 1
                        else:
                            continue

    return count


def xml2mask(xml_file, shape):
    """

    :param xml_file:
    :param shape:
    :return:
    """
    final_mask = np.zeros(shape, dtype=np.uint8)
    nucleus_dictionary = {'LSIL_Nucleus': 200,
                          'HSIL_Nucleus': 250,
                          'Nucleus_intermediate': 50,
                          'Nucleus_superficial': 100,
                          'Nucleus_parabasal': 150
                          }
    # 'Nucleus_metaplasia': 120,
    # 'Nucleus_hystiocyte': 130
    with open(xml_file) as fd:
        doc = xmltodict.parse(fd.read())
    d_item = doc['root']
    for i in d_item:
        if re.match('rois', i) is not None:
            roi_item = d_item[i]
            for j in roi_item:
                if re.match('roi', j) is not None:
                    roi = roi_item[j]
                    for l in range(len(roi)):
                        class_name = roi[l]['classname']
                        name = str(roi[l]['name'])
                        if name in nucleus_dictionary.keys():
                            label = nucleus_dictionary[name]
                        else:
                            continue

                        if re.search('ROI2DPolygon', class_name) is not None:
                            points = roi[l]['points']['point']
                            row_cords = []
                            col_cords = []
                            for point in points:
                                try:
                                    col_cords.append(np.double(point['pos_x']))
                                    row_cords.append(np.double(point['pos_y']))
                                except:
                                    continue
                            if not col_cords:
                                continue
                            fill_row_coords, fill_col_coords = poly2mask(row_cords, col_cords, shape)
                            final_mask[fill_row_coords, fill_col_coords] = label
                        elif re.search('ROI2DEllipse', class_name) is not None:
                            top_left_x = np.double(roi[l]['top_left']['pos_x'])
                            top_left_y = np.double(roi[l]['top_left']['pos_y'])
                            bottom_right_x = np.double(roi[l]['bottom_right']['pos_x'])
                            bottom_right_y = np.double(roi[l]['bottom_right']['pos_y'])

                            x_radius = abs(bottom_right_x - top_left_x) / 2
                            y_radius = abs(bottom_right_y - top_left_y) / 2
                            r = min(top_left_y, bottom_right_y) + y_radius
                            c = min(top_left_x, bottom_right_x) + x_radius
                            rr, cc = draw.ellipse(np.uint64(r),
                                                  np.uint64(c),
                                                  np.uint64(y_radius),
                                                  np.uint64(x_radius), shape)
                            rr = np.subtract(rr, 1)
                            cc = np.subtract(cc, 1)
                            final_mask[rr, cc] = label

    return final_mask


def poly2mask(vertex_row_coords_, vertex_col_coords_, shape):
    """

    :param vertex_row_coords_:
    :param vertex_col_coords_:
    :param shape:
    :return:
    """
    vertex_row_coords = np.asarray(vertex_row_coords_)
    vertex_col_coords = np.asarray(vertex_col_coords_)
    fill_row_coords, fill_col_coords = draw.polygon(vertex_row_coords, vertex_col_coords, shape)
    return fill_row_coords, fill_col_coords

def bmp2mask(bmp_file):
    """
    :bmp_file: .bmp file
    :return: 
    """
    bimg = cv2.imread(bmp_file)
    blue = bimg[:, :, 0]
    blue /= 255

    return blue
