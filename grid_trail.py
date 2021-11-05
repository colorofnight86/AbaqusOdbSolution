# -*- coding: utf-8 -*-
# @Time    : 2021/10/22 9:54
# @Author  : ColorOfNight
# @Email   : 852477089@qq.com
# @File    : grid_trail.py
# @Software: PyCharm
# @Description: 根据网格的中心点坐标生成轨迹
#

import math


def calc_time(point1, point2, velocity):
    """
    计算时间

    :param point1: 点1
    :param point2: 点2

    :param velocity: 速度
    :return: 时间
    """
    distance = math.sqrt(
        (point1[0] - point2[0]) * (point1[0] - point2[0]) + (point1[1] - point2[1]) * (point1[1] - point2[1]) +
        (point1[2] - point2[2]) * (point1[2] - point2[2]))
    return distance / velocity


def generate_line(time, point, flag, offset=0.0):
    """
    生成点的信息
    """
    return str(round(time + offset, 1)) + ',' + str(point[0]) + ',' + str(point[1]) + ',' + str(
        point[2] + offset) + ',' + str(flag) + '\n'


def read_from_file(file_path):
    """
    读取文件

    :param file_path: 文件路径
    :return: 网格中心点列表
    """
    with open(file_path) as f:
        content = f.readlines()
        result = [list(map(float, line.replace('\n', '').split(',')[1:])) for line in content]
        # print(result)
    return result


def generate_trail(grid, length_per_line, v1=1, v2=10):
    """

    :param grid: 网格列表
    :param length_per_line: 每条轨迹的网格个数
    :param v1: 速度1
    :param v2: 速度2
    :return: 字符串
    """
    time = 0.0
    file_content = generate_line(time, grid[0], 1)
    for i in range(1, len(grid)):
        p1 = grid[i - 1]
        p2 = grid[i]
        time = time + calc_time(p1, p2, v2) if i % length_per_line == 0 else time + calc_time(p1, p2, v1)
        if i % length_per_line == 0:
            file_content += generate_line(time, p2, 0, -0.1)
        file_content += generate_line(time, p2, 1)
        if (i + 1) % length_per_line == 0:
            file_content += generate_line(time, p2, 0, 0.1)
    print(file_content)
    return file_content


if __name__ == '__main__':
    lists = read_from_file('./centrenode.csv')
    content = generate_trail(lists, 16)
    with open('./trail.csv', 'w+') as f:
        f.write(content)
