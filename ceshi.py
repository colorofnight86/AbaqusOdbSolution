import os
import numpy as np


def refactor(list1):
    list1 = sorted(list1, key=lambda x: (x))


if __name__ == '__main__':
    lists = [0,1,2,3,4,5,6,7]
    # refactor(lists)
    str1 = ','.join(str(i) for i in lists)
    print(str1, lists)
    lists = [11j]
    print(lists)

    r, theta = np.mgrid[0:1:11j, 0:np.pi * 2:25j]
    print(r)