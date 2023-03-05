# -*- coding: utf-8 -*-
# @Time    : 2022/3/25 14:53
# @Author  : ColorOfNight
# @Email   : 852477089@qq.com
# @File    : 点在闭合轮廓里.py
# @Software: PyCharm
# @Description： 判断点是否在闭合的轮廓内，默认是一个凸多边形

import matplotlib.pyplot as plt
from line_util import *
import math
from random import uniform
import numpy as np

r = 2  # 半径


# 画圆弧
def circle(x, radius):
    return math.sqrt(abs(radius ** 2 - x ** 2))


# 判断点是否在线的上下左右的
def check_point(_p1, _p2, _p):
    _l, _r, _u, _d = 0, 0, 0, 0
    _x1, _y1, _x2, _y2, _x0, _y0 = _p1[0], _p1[1], _p2[0], _p2[1], _p[0], _p[1]
    if (_x1 <= _x0 <= _x2) or (_x2 <= _x0 <= _x1):
        if _x1 == _x2:
            _u, _d = 1, 1
        else:
            _y = (_x0 - _x2) / (_x1 - _x2) * (_y1 - _y2) + _y2
            if _y0 >= _y:
                _u = 1
            else:
                _d = 1
    if (_y1 <= _y0 <= _y2) or (_y2 <= _y0 <= _y1):
        if _y1 == _y2:
            _l, _r = 1, 1
        else:
            _x = (_y0 - _y2) / (_y1 - _y2) * (_x1 - _x2)
            if _x0 >= _x:
                _r = 1
            else:
                _l = 1
    return _l, _r, _u, _d


# 判断点是否在线里
def is_point_in_line(_point, _line):
    _line = close_line(_line)
    _i = 0
    left, right, up, down = 0, 0, 0, 0
    while _i < len(_line) - 1:
        _p1 = _line[_i]
        _p2 = _line[_i + 1]
        l_, r_, u_, d_ = check_point(_p1, _p2, _point)
        left += l_
        right += r_
        up += u_
        down += d_
        if (left > 0 and right > 0) or (up > 0 and down > 0):
            return True
        _i += 1
    return False


if __name__ == '__main__':
    x1 = np.arange(-r, r, 0.05)
    x2 = np.arange(r, -r, -0.05)
    y1 = [circle(x, r) for x in x1]
    y2 = [-circle(x, r) for x in x2]
    x = np.append(x1, x2)
    y = y1 + y2
    line1 = merge_line(x, y)
    line1 = close_line(line1)
    x, y = split_line(line1)
    point = [0, 0]

    x0 = [uniform(-r, r) for i in range(1000)]
    y0 = [uniform(-r, r) for i in range(1000)]
    # x0 = np.arange(-r, r, 0.05)
    # y0 = [circle(x, r - 0.05) for x in x0]

    points = merge_line(x0, y0)
    color = ['g' if is_point_in_line(point, line1) else 'r' for point in points]
    print(is_point_in_line([-2, circle(-2, r - 0.05)], line1))

    plt.axis('equal')  # 等轴
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(x, y, '--', color='b', marker='.', label='line1')
    # plt.scatter([-1.99], [circle(-2, r - 0.05)], c='r', s=50, marker='.', label='point')
    plt.scatter(x0, y0, c=color, s=30)
    plt.show()
