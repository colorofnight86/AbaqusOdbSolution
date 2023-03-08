# -*- coding: utf-8 -*-
# @Time    : 2021/11/15 21:46
# @Author  : ColorOfNight
# @Email   : 852477089@qq.com
# @File    : test.py
# @Software: PyCharm

import re


if __name__ == '__main__':
    list1 = [7, -4, 2, 5, 1, -6, -8, 3]
    list2 = [-7, 4, -2, -5, -1, 6, 8, -3]
    pair = [[10,4],[18,3],[5,1],[23,0],[1,2]]
    result = [item[1] for item in pair[:4]]
    print(result)

