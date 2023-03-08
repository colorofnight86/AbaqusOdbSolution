# -*- coding: utf-8 -*-
# @Time    : 2023/3/8 0:51
# @Author  : ColorOfNight
# @Email   : 852477089@qq.com
# @File    : 插值可视化.py
# @Software: PyCharm
import math
import time
from line_util import split_line
from paint_util import *


def two_linear_interpolation_2d(point, rect_points, rect_values):
    """
    两次线性插值法

    :return: 单个点的插值
    :param point: 待插值点
    :param rect_points: 已知矩形网格点，是4个点的列表
    :param rect_values: 已知参数
    """
    q0 = rect_points[0]
    q1 = rect_points[-1]
    x1, y1, x2, y2 = q0[0], q0[1], q1[0], q1[1]
    x, y = point[0], point[1]
    r1_value = (x2 - x) / (x2 - x1) * rect_values[0] + (x - x1) / (x2 - x1) * rect_values[1]  # r1[x,y1]
    r2_value = (x2 - x) / (x2 - x1) * rect_values[2] + (x - x1) / (x2 - x1) * rect_values[3]  # r2[x,y2]
    p_value = (y2 - y) / (y2 - y1) * r1_value + (y - y1) / (y2 - y1) * r2_value  # p[x,y,z1]

    return p_value


def two_linear_interpolations_2d(points, cube_points, cube_values, variable_bound=False):
    """
    三线性插值的批处理版本，除points和variable_bound外其它参数跟two_linear_interpolation_2d一致

    :param points: 待插值点的列表
    :param cube_points:
    :param cube_values:
    :param variable_bound: 默认一个cube_points对应多个points，为True时每一个一个cube_points对应一个point
    :return: 插值的列表
    """
    _values = []
    start_time = time.time()
    for idx in range(len(points)):
        if not variable_bound:
            _values.append(two_linear_interpolation_2d(points[idx], cube_points, cube_values))
        else:
            _values.append(two_linear_interpolation_2d(points[idx], cube_points[idx], cube_values[idx]))
    end_time = time.time()
    print('耗时:', end_time - start_time, 's')
    return _values


def distance_inverse_interpolation_2d(point, existed_points, existed_values, power=2.0):
    """
    距离反比插值法，2d版

    :return: 单个点的插值
    :param power: 距离的指数次方，默认为2
    :param point: 待插值点
    :param existed_points: 已知点
    :param existed_values: 已知值
    """

    def distance(p1, p2):  # 计算欧几里得距离
        dist = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
        dist = math.sqrt(dist)
        return dist

    distance_list = []
    for idx, point2 in enumerate(existed_points):
        if distance(point, point2) == 0:  # 跟某个点重合，直接返回该点的数值
            return existed_values[idx]
        distance_list.append(1 / (distance(point, point2) ** power))  # 权重列表，倒数

    # 计算权重
    distance_sum = sum(distance_list)
    weight_list = []
    for distance in distance_list:
        weight_list.append(distance / distance_sum)
    target_value = 0.0
    for idx in range(len(existed_points)):
        target_value += weight_list[idx] * existed_values[idx]  # 加权和
    return target_value


def distance_inverse_interpolations_2d(points, existed_points, existed_values, power=2.0, variable_bound=False):
    """
    距离反比加权插值的批量版本，除points外其它参数跟distance_inverse_interpolation_2d一致

    :param points: 待插值点列表
    :param existed_points:
    :param existed_values:
    :param power:
    :param variable_bound:
    :return: 插值的列表
    """
    _values = []
    start_time = time.time()
    for idx in range(len(points)):
        if not variable_bound:
            _values.append(distance_inverse_interpolation_2d(points[idx], existed_points, existed_values, power))
        else:
            _values.append(distance_inverse_interpolation_2d(points[idx], existed_points[idx], existed_values[idx], power))
    end_time = time.time()
    print(power, '耗时:', end_time - start_time, 's')
    return _values


def generate_test_points(rect, num):
    """
    生成均匀的测试目标点

    :param rect: 矩形四点，首位是矩形的两个对角点
    :param num: 每边的点数
    """
    point_start = rect[0]
    point_end = rect[-1]
    target_test_points = []  # 测试用的目标点

    x_0 = point_start[0]
    y_0 = point_start[1]
    inr_x = (point_end[0] - point_start[0]) / num
    inr_y = (point_end[1] - point_start[1]) / num

    for i in range(0, num+1):
        for j in range(0, num+1):
            point_x = inr_x * i + x_0
            point_y = inr_y * j + y_0
            target_point = [point_x, point_y]
            target_test_points.append(target_point)

    return target_test_points


def find_nearest_four_points(point_list, target_list, value_list):
    """
    寻找最近的四个点

    """
    result_lists = []
    value_lists = []

    for point in point_list:
        distance_list = [[distance2(point, target_list[i]), i] for i in range(len(target_list))]  # [[distance, i]]的列表
        distance_list = sorted(distance_list, key=lambda x: x[0])  # 按距离从小到大排序
        index_list = [item[1] for item in distance_list[:4]]
        result_lists.append(get_ele_by_index(target_list, index_list))
        value_lists.append(get_ele_by_index(value_list, index_list))
    return result_lists, value_lists


def get_ele_by_index(ele_list, index_list):
    """
    根据索引列表获取元素

    :param ele_list: 元素列表
    :param index_list: 索引列表
    """
    result_list = []
    length = len(ele_list)
    for idx in index_list:
        if idx < length:
            result_list.append(ele_list[idx])
    return result_list

def distance2(p1, p2):
    """
    计算欧几里得距离的平方

    :param p1:
    :param p2:
    :return:
    """
    dist = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
    return dist


if __name__ == '__main__':
    test_points_2d_1 = [[0, 0], [10, 0], [0, 10], [10, 10]]
    test_values_1 = [7, 4, 2, 10]
    test_points_2d_2 = [[-10, 0], [0, 0], [-10, 10], [0, 10]]
    test_values_2 = [1, 7, 3, 2]
    test_points_2d_3 = [[-10, -10], [0, -10], [-10, 0], [0, 0]]
    test_values_3 = [5, 6, 1, 7]
    test_points_2d_4 = [[0, -10], [10, -10], [0, 0], [10, 0]]
    test_values_4 = [6, 3, 7, 4]

    test_points = [[-10, -10], [-10, 0], [-10, 10], [0, -10], [0, 0], [0, 10], [10, -10], [10, 0], [10, 10]]
    test_values = [5, 1, 3, 6, 7, 2, 3, 4, 10]

    target_points1 = generate_test_points(test_points_2d_1, 50)
    target_points2 = generate_test_points(test_points_2d_2, 50)
    target_points3 = generate_test_points(test_points_2d_3, 50)
    target_points4 = generate_test_points(test_points_2d_4, 50)

    # 多种方法实现插值
    # 双线性插值
    values = two_linear_interpolations_2d(target_points1, test_points_2d_1, test_values_1, variable_bound=False)
    # values1 = two_linear_interpolations_2d(target_points, test_points_2d_1, test_values_1, variable_bound=False)
    # values2 = two_linear_interpolations_2d(target_points2, test_points_2d_2, test_values_2, variable_bound=False)
    # values3 = two_linear_interpolations_2d(target_points3, test_points_2d_3, test_values_3, variable_bound=False)
    # values4 = two_linear_interpolations_2d(target_points4, test_points_2d_4, test_values_4, variable_bound=False)
    # 距离反比插值
    # values1 = distance_inverse_interpolations_2d(target_points1, test_points_2d_1, test_values_1, variable_bound=False)
    # values2 = distance_inverse_interpolations_2d(target_points2, test_points_2d_2, test_values_2, variable_bound=False)
    # values3 = distance_inverse_interpolations_2d(target_points3, test_points_2d_3, test_values_3, variable_bound=False)
    # values4 = distance_inverse_interpolations_2d(target_points4, test_points_2d_4, test_values_4, variable_bound=False)

    # 优化距离反比插值
    # 寻找最近的四个点，根据最近的四个点进行插值
    test_points_2d_5, test_values_5 = find_nearest_four_points(target_points1, test_points, test_values)
    test_points_2d_6, test_values_6 = find_nearest_four_points(target_points2, test_points, test_values)
    test_points_2d_7, test_values_7 = find_nearest_four_points(target_points3, test_points, test_values)
    test_points_2d_8, test_values_8 = find_nearest_four_points(target_points4, test_points, test_values)
    values1 = distance_inverse_interpolations_2d(target_points1, test_points_2d_5, test_values_5, variable_bound=True)
    values2 = distance_inverse_interpolations_2d(target_points2, test_points_2d_6, test_values_6, variable_bound=True)
    values3 = distance_inverse_interpolations_2d(target_points3, test_points_2d_7, test_values_7, variable_bound=True)
    values4 = distance_inverse_interpolations_2d(target_points4, test_points_2d_8, test_values_8, variable_bound=True)




    # 将values赋为点的z坐标，并画三维点云，直观显示插值效果
    init_plt()
    x1, y1 = split_line(target_points1)
    x2, y2 = split_line(target_points2)
    x3, y3 = split_line(target_points3)
    x4, y4 = split_line(target_points4)
    z, z1, z2, z3, z4 = np.array(values), np.array(values1), np.array(values2), np.array(values3), np.array(values4)
    # plotXYZ(x1, y1, z1+1, 3)
    plotXYZ(x1, y1, z1, 3)
    plotXYZ(x2, y2, z2, 3)
    plotXYZ(x3, y3, z3, 3)
    plotXYZ(x4, y4, z4, 3)
    plt_show()
