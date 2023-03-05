# -*- coding: utf-8 -*-
# @Time    : 2021/11/8 15:34
# @Author  : ColorOfNight
# @Email   : 852477089@qq.com
# @File    : grid_division.py
# @Software: PyCharm
# @Description: plt的3d绘制测试

from matplotlib import pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
import numpy as np

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import matplotlib.colors
    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D

    def midpoints(x):
        sl = ()
        for i in range(x.ndim):
            x = (x[sl + np.index_exp[:-1]] + x[sl + np.index_exp[1:]]) / 2.0
            sl += np.index_exp[:]
        return x


    # prepare some coordinates, and attach rgb values to each
    r, theta, z = np.mgrid[0:1:11j, 0:np.pi * 2:25j, -0.5:0.5:11j]
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    rc, thetac, zc = midpoints(r), midpoints(theta), midpoints(z)

    # define a wobbly torus about [0.7, *, 0]
    sphere = (rc - 0.7) ** 2 + (zc + 0.2 * np.cos(thetac * 2)) ** 2 < 0.2 ** 2
    print(sphere)

    # combine the color components
    hsv = np.zeros(sphere.shape + (3,))
    hsv[..., 0] = thetac / (np.pi * 2)
    hsv[..., 1] = rc
    hsv[..., 2] = zc + 0.5
    colors = matplotlib.colors.hsv_to_rgb(hsv)

    # and plot everything
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.voxels(x, y, z, sphere,
              facecolors=colors,
              edgecolors=np.clip(2 * colors - 0.5, 0, 1),  # brighter
              linewidth=0.5,
              shade=False)
    plt.rcParams['axes.unicode_minus'] = False

    plt.show()

    # plt.ion()
    fig = plt.figure()
    # 创建3d图形的两种方式
    # 1、将figure变为3d
    ax = Axes3D(fig)
    ax.view_init(7, -80)
    # 2、ax = fig.add_subplot(221, projection='3d')

    # 定义x, y
    x = np.arange(-4, 4, 0.26)
    y = np.arange(-4, 4, 0.26)

    # 生成网格数据，相当于笛卡尔积
    X, Y = np.meshgrid(x, y)
    # 计算每个点对的长度
    R = np.sqrt(X ** 2 + Y ** 2)
    Z = np.sin(R)

    # 绘制3D曲面
    ax.scatter(X, Y, Z, c="#00CED1", marker='^')
    # ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('rainbow'))
    # rstride:行之间的跨度  cstride:列之间的跨度
    # rcount:设置间隔个数，默认50个，ccount:列的间隔个数  不能与上面两个参数同时出现
    # cmap参数可以控制三维曲面的颜色组合, 一般三维曲面就是 rainbow 的，可以使用collwarm
    # 你也可以修改 rainbow 为 coolwarm, 验证我的结论

    # 底部的投影
    ax.contour(X, Y, Z, zdir='z', offset=-1, cmap=plt.get_cmap('coolwarm'))
    # zdir 可选 'z'|'x'|'y'| 分别表示投影到z,x,y平面
    # zdir = 'z', offset = -1 表示投影到z = -1上

    # 设置z轴的维度，x,y类似
    ax.set_zlim(-2, 2)
    plt.show()


# plt.ioff()
# plt.show()