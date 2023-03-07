# -*- coding: utf-8 -*-
# @Time    : 2021/10/20 9:00
# @Author  : ColorOfNight
# @Email   : 852477089@qq.com
# @File    : hexahedral_volume.py
# @Software: PyCharm
# @Description: 求凸六面体体积

# 用于网格体积的获取
from abaqus import *
import mesh
import part
import numpy as np
from numpy.linalg import *


def tetrahedral_volume(tetrahedron):
    """
                  |x1 x2 x3 x4|
    V(A,B,C,D) =  |y1 y2 y3 y4|
                  |z1 z2 z3 z4|
                  | 1  1  1  1|
    四面体体积公式V=|V(A,B,C,D)|/6

    :param tetrahedron: 四面体的四个点
    :return: 四面体体积
    """
    tetrahedron_np = np.array([[tetrahedron[0][0], tetrahedron[1][0], tetrahedron[2][0], tetrahedron[3][0]],
                               [tetrahedron[0][1], tetrahedron[1][1], tetrahedron[2][1], tetrahedron[3][1]],
                               [tetrahedron[0][2], tetrahedron[1][2], tetrahedron[2][2], tetrahedron[3][2]],
                               [1, 1, 1, 1]])
    return det(tetrahedron_np) / 6


def find_point(lists):
    """
    找到符号与其他符号不同的那个点

    :param lists: 列表
    :return: 索引，不存在该点时返回-1
    """
    pos_index, neg_index = 0, 0
    pos_count, neg_count = 0, 0
    for i in range(len(lists)):
        if lists[i] > 0:
            pos_count += 1
            pos_index = i
        if lists[i] < 0:
            neg_count += 1
            neg_index = i
    if pos_count > 0 and neg_count > 0:
        if pos_count == 1:
            return pos_index
        if neg_count == 1:
            return neg_index
    return -1


def is_surface(lists):
    """
    判断是否为表面

    :param lists:
    :return: 判断结果
    """
    pos_count, neg_count = 0, 0
    for i in range(len(lists)):
        if lists[i] > 0:
            pos_count += 1
        if lists[i] < 0:
            neg_count += 1
    if pos_count == 0 or neg_count == 0:
        return True
    return False


def find_four_point(polyhedron):
    """
    寻找四个异面的点

    :param polyhedron: 多面体点集
    :return: 四个异面的点, 剩余的点
    """
    if len(polyhedron) > 4:
        temp = polyhedron.copy()
        for i in range(0, len(polyhedron) - 2):
            temp.remove(polyhedron[i])
            for j in range(i + 1, len(polyhedron) - 1):
                temp.remove(polyhedron[j])
                for k in range(j + 1, len(polyhedron)):
                    temp.remove(polyhedron[k])
                    list_diff = [tetrahedral_volume([polyhedron[i], polyhedron[j], polyhedron[k], point]) for point in
                                 temp]
                    if find_point(list_diff) >= 0:
                        index = find_point(list_diff)
                        p1 = polyhedron[i]
                        p2 = polyhedron[j]
                        p3 = polyhedron[k]
                        p4 = temp[index]
                        polyhedron.remove(p4)
                        return [p1, p2, p3, p4], polyhedron
                    temp.append(polyhedron[k])
                temp.append(polyhedron[j])
            temp.append(polyhedron[i])
    return polyhedron, []


def polyhedral_volume(polyhedral):
    """
    求多面体体积

    :param polyhedral: 多面体的点列表
    :return: 多面体体积
    """
    # print(len(polyhedral))
    # if len(polyhedral) <= 3:
    #     return 0
    # if len(polyhedral) == 4 and tetrahedral_volume(polyhedral) == 0.0:
    #     print('共面')
    #     print(polyhedral)
    #     return 0
    # points, polyhedron = find_four_point(polyhedral)
    # volume = abs(tetrahedral_volume(points))
    # return volume + polyhedral_volume(polyhedron)
    tetrahedron1 = [polyhedral[0], polyhedral[1], polyhedral[2], polyhedral[4]]
    tetrahedron2 = [polyhedral[0], polyhedral[2], polyhedral[3], polyhedral[4]]
    volume = abs(tetrahedral_volume(tetrahedron1)) + abs(tetrahedral_volume(tetrahedron2))
    return volume


def find_surfaces(point_list):
    """
    寻找表面

    :param point_list: 六面体点集
    :return: 表面列表
    """
    surfaces = []
    length = len(point_list)
    for i in range(0, length - 3):
        for j in range(i + 1, length - 2):
            for k in range(j + 1, length - 1):
                for l in range(k + 1, length):
                    temp = point_list.copy()
                    p1 = point_list[i]
                    p2 = point_list[j]
                    p3 = point_list[k]
                    p4 = point_list[l]
                    surface = [p1, p2, p3, p4]
                    temp.remove(p1)
                    temp.remove(p2)
                    temp.remove(p3)
                    temp.remove(p4)
                    diff_list = [tetrahedral_volume([p1, p2, p3, point]) for point in temp]

                    # 四点共面且为表面
                    if tetrahedral_volume(surface) == 0:
                        print("11")
                        if is_surface(diff_list):
                            surfaces.append([p1, p2, p3, p4])
    print(len(surfaces), 'surfaces')
    return surfaces


def hexahedral_volume(hexahedron):
    """
    计算六面体体积

    :param hexahedron: 六面体的8个点坐标列表
    :return: 体积
    """
    # 找中心点
    x, y, z = 0, 0, 0
    for point in hexahedron:
        x += point[0]
        y += point[1]
        z += point[2]
    center_point = [x / 8, y / 8, z / 8]

    # 找六个表面
    # surface_list = find_surfaces(hexahedron)
    if(len(hexahedron) != 8):
        return 0, []
    surface_list = [[hexahedron[0], hexahedron[1], hexahedron[2], hexahedron[3]],
                    [hexahedron[4], hexahedron[5], hexahedron[6], hexahedron[7]],
                    [hexahedron[0], hexahedron[1], hexahedron[5], hexahedron[4]],
                    [hexahedron[1], hexahedron[2], hexahedron[6], hexahedron[5]],
                    [hexahedron[2], hexahedron[3], hexahedron[7], hexahedron[6]],
                    [hexahedron[3], hexahedron[0], hexahedron[4], hexahedron[7]]]

    # 求六个四棱锥的体积
    volume = 0
    i = 0
    for surface in surface_list:
        i += 1
        surface.append(center_point)
        v = polyhedral_volume(surface)
        # print(i, v)
        volume += v
    return volume, center_point


if __name__ == '__main__':
    nodee = mdb.models['Model-1'].parts['jietou01'].nodes
    elementt = mdb.models['Model-1'].parts['jietou01'].elements
    volume = []
    filepath_VOLUMES = "D:\\003simulation\\001abaqus\\zmb/volumes.csv"
    file_VOLUMES = open(filepath_VOLUMES, 'w+')
    filepath_centrenode = "D:\\003simulation\\001abaqus\\zmb/centrenode.csv"
    file_centrenode = open(filepath_centrenode, 'w+')
    for num in range(0, 480):
        ploy_nodes_num = elementt[num].connectivity
        ploy_node = []
        ploy_node.append(nodee[ploy_nodes_num[0]].coordinates)
        ploy_node.append(nodee[ploy_nodes_num[1]].coordinates)
        ploy_node.append(nodee[ploy_nodes_num[2]].coordinates)
        ploy_node.append(nodee[ploy_nodes_num[3]].coordinates)
        ploy_node.append(nodee[ploy_nodes_num[4]].coordinates)
        ploy_node.append(nodee[ploy_nodes_num[5]].coordinates)
        ploy_node.append(nodee[ploy_nodes_num[6]].coordinates)
        ploy_node.append(nodee[ploy_nodes_num[7]].coordinates)
        str_volume, str_cent = hexahedral_volume(ploy_node)
        volume.append(str_volume)
        file_VOLUMES.write(str(num + 1) + ',' + str(volume[num]) + '\n')
        #file_nodes.write(str(num + 1) + ',' + str(ploy_node) + '\n')
        file_centrenode.write(str(num + 1) + ',' + str(str_cent) + '\n')

    file_VOLUMES.close()
    file_centrenode.close()
    print('congratulation!!')
