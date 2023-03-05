# -*- coding: utf-8 -*-
# @Time    : 2022/3/25 15:01
# @Author  : ColorOfNight
# @Email   : 852477089@qq.com
# @File    : line_util.py
# @Software: PyCharm
# @Description: 工具类
import math
from random import randint as ri
import numpy as np


def split_line(_line, axis=2, nparray=False):
    """
    将线拆分成x,y[,z]轴

    :param nparray: 是否返回nparray的格式
    :param axis: 轴的数量
    :param _line: list-需要拆分的点集
    :return:(list, list): x,y[,z]轴
    """
    _x, _y = [], []
    _z = []
    for _point in _line:
        _x.append(_point[0])
        _y.append(_point[1])
        if axis == 3:
            _z.append(_point[2])
    if nparray:
        _x, _y, _z = np.array(_x), np.array(_y), np.array(_z)
    if axis == 3:
        return _x, _y, _z
    return _x, _y


def merge_line(_x, _y, _z=None):
    """
    将x,y合并成线

    :param _z: list: z轴
    :param _x: list: x轴
    :param _y: list: y轴
    :return: list: 线
    """
    _line = []
    if len(_x) != len(_y):
        return _line
    for _i in range(len(_x)):
        if _z is not None:
            _line.append([_x[_i], _y[_i], _z[_i]])
        else:
            _line.append([_x[_i], _y[_i]])
    return _line


def close_line(_line: list):
    if len(_line) > 1 and _line[0] != _line[-1]:
        _line.append(_line[0])
    return _line.copy()


def load_data(filepath, filename, num=-1, data_type='float'):
    """
    读取数据

    :param filepath: 文件路径 str
    :param filename: 文件名 str
    :param num: 读取数据的个数，小于0表示读取全部
    :param data_type: 读取的数据类型
    :return: 数据列表，去编号
    """
    with open(filepath + filename, mode='r', newline='\n') as f:
        file = f.readlines()
        num = min(num, len(file)) if num > 0 else len(file)
        node_list = [[int(x) for x in info.replace('\n', '').split(',')[1:]] for info in file[:num]] if \
            data_type == 'int' else [[float(x) for x in info.replace('\n', '').split(',')[1:]] for info in file[:num]]
    node_list.insert(0, [0] * len(node_list[0]))
    print('\n读取' + filename, ':', node_list[:min(20, num)], '……' if num > 20 else '')
    print('读取数量:', len(node_list) - 1)
    return node_list, num


# 计算两点间的距离
def calc_distance(p1, p2, root=2):
    distance = (p1[0] - p2[0]) ** 2 + ((p1[1] - p2[1]) ** 2) / 4 + (p1[0] - p2[0]) ** 2
    return distance ** (1 / root)


# 生成随机颜色/生成固定的N种颜色
def get_color(num=None):
    if num is None:
        color: int
        color1 = ri(16, 255)
        color2 = ri(16, 255)
        color3 = ri(16, 255)
        color1 = hex(color1)
        color2 = hex(color2)
        color3 = hex(color3)
        ans = "#" + color1[2:] + color2[2:] + color3[2:]
        return ans
    # else:
    #     ans = []
    #     # step = int(255 / num)
    #     # color_value = [16+i*step for i in range(num)]
    #     for i in range(num):
    #         # color1 = hex(color_value[i])
    #         # color2 = hex(color_value[(i+int(num/3))%num])
    #         # color3 = hex(color_value[(i+int(num/3*2))%num])
    #         # ans.app end("#" + color1[2:] + color2[2:] + color3[2:])
    #         ans.append(get_color())
    color = ["#ff00ff", "#1e90ff", "#808080", "#dcdcdc", "#2f4f4f", "#556b2f", "#6b8e23", "#a0522d", "#a52a2a",
             "#483d8b", "#5f9ea0", "#008000", "#3cb371", "#bdb76b", "#4682b4", "#000080", "#d2691e", "#9acd32",
             "#32cd32", "#daa520", "#8fbc8f", "#8b008b", "#9932cc", "#ff0000", "#00ced1", "#ff8c00", "#ffd700",
             "#c71585", "#0000cd", "#00ff00", "#00ff7f", "#dc143c", "#00bfff", "#f4a460", "#0000ff", "#a020f0",
             "#adff2f", "#ff6347", "#db7093", "#fa8072", "#ffff54", "#dda0dd", "#87ceeb", "#7b68ee", "#ee82ee",
             "#98fb98", "#7fffd4", "#ffdab9", "#ff69b4", "#ffc0cb"]
    return color[:num]


# 计算聚类的中心点
def calc_cluster_center(cluster):
    num = len(cluster)
    if num == 0:
        return cluster
    center_point = [0, 0, 0]
    for point in cluster:
        center_point[0] += point[0]
        center_point[1] += point[1]
        center_point[2] += point[2]
    center_point[0] /= num
    center_point[1] /= num
    center_point[2] /= num
    return center_point


# 判断两个列表是否一致
def is_list_equal(list1, list2):
    if len(list1) != len(list2):
        print("两列表长度不一致")
        return False
    for _i in range(len(list1)):
        point1 = list1[_i]
        point2 = list2[_i]
        if point1[0] != point2[0] or point1[1] != point2[1] or point1[2] != point2[2]:
            return False
    return True


def get_center_point(elements_list, point_list):
    """
    获取立方体中心点的坐标

    :param elements_list:
    :param point_list:
    :return:
    """
    center_points = []
    for element in elements_list:
        points = [point_list[label] for label in element]
        x, y, z = 0.0, 0.0, 0.0
        for point in points:
            x += point[0]
            y += point[1]
            z += point[2]
        center_points.append([x / 8, y / 8, z / 8])
    return center_points


if __name__ == '__main__':
    line = [[1, 1], [2, 2], [3, 3]]
    line1 = close_line(line).copy()
    line[0] = [1, -1]
    print(line1)
