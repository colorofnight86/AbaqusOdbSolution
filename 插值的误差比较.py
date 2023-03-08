# -*- coding: utf-8 -*-
# @Time    : 2023/3/5 21:47
# @Author  : ColorOfNight
# @Email   : 852477089@qq.com
# @File    : 插值的误差比较.py
# @Software: PyCharm
# @Description: 对比双线性插值和距离反比加权插值的误差
import time
from interpolation_test import get_point_list
import math


def three_linear_interpolation(point, cube_points, cube_values):
    """
    三次线性插值法

    :return: 单个点的插值
    :param point: 待插值点
    :param cube_points: 已知立方体网格点，是8个点的列表
    :param cube_values: 已知参数
    """
    q0 = cube_points[0]
    q1 = cube_points[-1]
    x1, y1, z1, x2, y2, z2 = q0[0], q0[1], q0[2], q1[0], q1[1], q1[2]
    x, y, z = point[0], point[1], point[2]
    r1_value = (x2 - x) / (x2 - x1) * cube_values[0] + (x - x1) / (x2 - x1) * cube_values[1]  # r1[x,y1,z1]
    r2_value = (x2 - x) / (x2 - x1) * cube_values[2] + (x - x1) / (x2 - x1) * cube_values[3]  # r2[x,y2,z1]
    p1_value = (y2 - y) / (y2 - y1) * r1_value + (y - y1) / (y2 - y1) * r2_value  # p1[x,y,z1]
    r3_value = (x2 - x) / (x2 - x1) * cube_values[4] + (x - x1) / (x2 - x1) * cube_values[5]  # r3[x,y1,z2]
    r4_value = (x2 - x) / (x2 - x1) * cube_values[6] + (x - x1) / (x2 - x1) * cube_values[7]  # r4[x,y2,z2]
    p2_value = (y2 - y) / (y2 - y1) * r3_value + (y - y1) / (y2 - y1) * r4_value  # p2[x,y,z2]
    p_value = (z2 - z) / (z2 - z1) * p1_value + (z - z1) / (z2 - z1) * p2_value

    return p_value


def three_linear_interpolations(points, cube_points, cube_values, variable_bound=False):
    """
    三线性插值的批处理版本，除points和variable_bound外其它参数跟three_linear_interpolation一致

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
            _values.append(three_linear_interpolation(points[idx], cube_points, cube_values))
        else:
            _values.append(three_linear_interpolation(points[idx], cube_points[idx], cube_values[idx]))
    end_time = time.time()
    print('耗时:', end_time - start_time, 's')
    return _values


def distance_inverse_interpolation(point, existed_points, existed_values, power=2.0):
    """
    距离反比插值法

    :return: 单个点的插值
    :param power: 距离的指数次方，默认为2
    :param point: 待插值点
    :param existed_points: 已知点
    :param existed_values: 已知值
    """

    def distance(p1, p2):  # 计算欧几里得距离
        dist = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2
        dist = math.sqrt(dist)
        return dist

    def distance2(p1, p2):  # 计算欧几里得距离
        dist = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2
        return dist

    if power == 2.0:
        distance_list = [1 / distance2(point, point2) for point2 in existed_points]
    else:
        distance_list = [1 / (distance(point, point2) ** power) for point2 in existed_points]

    # 计算权重
    distance_sum = sum(distance_list)
    weight_list = []
    for idx, distance in enumerate(distance_list):
        if distance == 0:  # 跟某个点重合，直接返回该点的数值
            return existed_values[idx]
        weight_list.append(distance / distance_sum)
    target_value = 0.0
    for idx in range(len(existed_points)):
        target_value += weight_list[idx] * existed_values[idx]
    return target_value


def distance_inverse_interpolations(points, existed_points, existed_values, power=2.0, variable_bound=False):
    """
    距离反比加权插值的批量版本，除points外其它参数跟distance_inverse_interpolation一致

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
            _values.append(distance_inverse_interpolation(points[idx], existed_points, existed_values, power))
        else:
            _values.append(distance_inverse_interpolation(points[idx], existed_points[idx], existed_values[idx], power))
    end_time = time.time()
    print(power, '耗时:', end_time - start_time, 's')
    return _values


def compare_list(l1, l2):
    """
    比较两组数据的偏差，输出

    :param l1:
    :param l2:
    """
    length = len(l1)
    diff_list = [(l1[idx] - l2[idx]) / l1[idx] for idx in range(length)]  # 误差列表
    sum_diff = sum(diff_list)
    avg_diff = sum([abs(x) for x in diff_list]) / length
    RMSE = math.sqrt(sum([x * x for x in diff_list]) / length)
    print('sum_diff:', sum_diff, 'avg_diff:', avg_diff, 'RMSE:', RMSE)


def compare(list1, list2):
    result = 0
    num = 0
    diff_list = []
    for idx in range(len(list1)):
        x1 = list1[idx]
        x2 = list2[idx]
        num += 1
        diff = abs(x2 - x1) / x1
        diff_list.append(diff)
        result += diff
    print(result / num)


if __name__ == '__main__':
    test_points_3d = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1]]
    test_values = [7, 4, 2, 5, 1, 6, 8, 3]

    point_start = test_points_3d[0]
    point_end = test_points_3d[-1]
    target_points = []

    n = 10  # 每条边的点数

    x_0 = point_start[0]
    y_0 = point_start[1]
    z_0 = point_start[2]
    inr_x = (point_end[0] - point_start[0]) / n
    inr_y = (point_end[1] - point_start[1]) / n
    inr_z = (point_end[2] - point_start[2]) / n
    for i in range(1, n):
        for j in range(1, n):
            for k in range(1, n):
                point_x = inr_x * i + x_0
                point_y = inr_y * j + y_0
                point_z = inr_z * k + z_0
                target_point = [point_x, point_y, point_z]
                target_points.append(target_point)

    p, p_list, para = get_point_list(10000)

    # values = three_linear_interpolations(target_points, test_points_3d, test_values)
    values = three_linear_interpolations(p, p_list, para, variable_bound=True)
    for i in range(0, 30):
        pow = 1 + i * 0.1
        # values1 = distance_inverse_interpolations(target_points, test_points_3d, test_values, pow)
        values1 = distance_inverse_interpolations(p, p_list, para, pow, variable_bound=True)
        compare_list(values, values1)

    # values1 = distance_inverse_interpolations(p, p_list, para, variable_bound=True)
    # compare_list(values, values1)
    # compare(values, values1)
