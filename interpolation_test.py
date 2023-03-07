# -*- coding: utf-8 -*-
# @Time    : 2021/11/5 10:20
# @Author  : ColorOfNight
# @Email   : 852477089@qq.com
# @File    : interpolation_test.py
# @Software: PyCharm
# @Description: 比较三次线性插值和反距离差值的偏差

import math
import random
import time


def inverse_distance_weight(point, points, values, select=2):
    """
    用距离平方的倒数求目标点处的插值

    :param point: 目标点
    :param points: 近邻点
    :param values: 近邻点的值
    :param select: 距离倒数的幂级
    :return: 插值
    """
    n = len(points)
    value = 0
    if select == 1:
        distance_list = [distance(point, point2) for point2 in points]
    elif select == 3:
        distance_list = [distance(point, point2)*distance2(point, point2) for point2 in points]
    else:
        distance_list = [distance2(point, point2) for point2 in points]
    weight_list = [0.0] * n
    weight_sum = 0
    for i in range(n):
        # 如果距离为0，将权重设为1，其他设为0
        if distance_list[i] == 0:
            weight_list = [0] * n
            weight_list[i] = 1
            weight_sum = 1
            break
        weight = 1 / distance_list[i]
        weight_list[i] = weight
        weight_sum += weight
    for i in range(n):
        weight = weight_list[i] / weight_sum
        # value = (weight_list[i]/weight_sum, values[i])
        value = value + values[i] * weight
    return value


def distance(p1, p2):
    """
    两点间的欧式距离

    :param p1: 点1
    :param p2: 点2
    """
    return math.sqrt(distance2(p1, p2))


def distance2(p1, p2):
    """
    两点间欧式距离的平方

    :param p1: 点1
    :param p2: 点2
    """
    return (p1[2] - p2[2]) * (p1[2] - p2[2]) + (p1[1] - p2[1]) * (p1[1] - p2[1]) + (p1[0] - p2[0]) * (p1[0] - p2[0])


def get_point_list(num):
    points = []
    inner_points = []
    values = []
    for i in range(num):
        boundary = [random.uniform(1, 5) for i in range(4)]
        x, y, z, l = boundary[0], boundary[1], boundary[2], boundary[3]
        point = [[x, y, z], [x + l, y, z], [x, y + l, z], [x + l, y + l, z], [x, y, z + l], [x + l, y, z + l],
                 [x, y + l, z + l], [x + l, y + l, z + l]]
        center_point = [x + random.random() * l, y + random.random() * l, z + random.random() * l]
        value = [random.randint(1, 50) for i in range(8)]
        points.append(point)
        inner_points.append(center_point)
        values.append(value)
    return inner_points, points, values


def inverse_distance_interpolation(points, boundaries, values, select=2):
    start_time = time.time()
    result = [0.0] * len(points)
    for i in range(len(points)):
        point = points[i]
        point_list = boundaries[i]
        value = values[i]
        result[i] = inverse_distance_weight(point, point_list, value, select)
    end_time = time.time()
    print(select, '耗时:', end_time-start_time, 's')
    return result


def three_linear_interpolation(points, boundaries, values):
    result = [0.0] * len(points)
    for i in range(len(points)):
        point = points[i]
        boundary = boundaries[i]
        x, y, z = point[0], point[1], point[2]
        x_, y_, z_, l_ = boundary[0][0], boundary[0][1], boundary[0][2], boundary[7][0] - boundary[0][0]
        value = values[i]
        r1 = (x_ + l_ - x) / l_ * value[0] + (x - x_) / l_ * value[1]
        r2 = (x_ + l_ - x) / l_ * value[2] + (x - x_) / l_ * value[3]
        q1 = (y_ + l_ - y) / l_ * r1 + (y - y_) / l_ * r2
        r3 = (x_ + l_ - x) / l_ * value[4] + (x - x_) / l_ * value[5]
        r4 = (x_ + l_ - x) / l_ * value[6] + (x - x_) / l_ * value[7]
        q2 = (y_ + l_ - y) / l_ * r3 + (y - y_) / l_ * r4
        p1 = (z_ + l_ - z) / l_ * q1 + (z - z_) / l_ * q2
        result[i] = p1
    return result


def compare(list1, list2):
    result = 0
    n = 0
    for i in range(len(list1)):
        x1 = list1[i]
        x2 = list2[i]
        n += 1
        result += abs(x2-x1)/x1
    return result/n


if __name__ == '__main__':
    p, p_list, para = get_point_list(10000)
    res1 = inverse_distance_interpolation(p, p_list, para, 1)
    res2 = inverse_distance_interpolation(p, p_list, para, 2)
    res3 = inverse_distance_interpolation(p, p_list, para, 3)
    res = three_linear_interpolation(p, p_list, para)
    print(compare(res, res1))
    print(compare(res, res2))
    print(compare(res, res3))
