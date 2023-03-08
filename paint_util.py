# -*- coding: utf-8 -*-
# @Time    : 2022/9/6 12:44
# @Author  : ColorOfNight
# @Email   : 852477089@qq.com
# @File    : paint_util.py
# @Software: PyCharm
# @Description: plt绘制相关的组件工具

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import line_util as util
import numpy as np

ax = None


def init_plt():
    """
    初始化plt相关的配置

    """
    # legend
    # plt.legend(loc=2)

    # overlapping
    # plt.tight_layout()

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    plt.rcParams['axes.unicode_minus'] = False


def plotSample(reverse=False):
    """
    绘制样例

    :return: canvas
    """
    # 清屏
    # plt.cla()
    # 获取绘图并绘制
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.set_xlim([-1, 6])
    ax.set_ylim([-1, 6])
    if reverse:
        ax.plot([5, 4, 3, 2, 1, 0], 'o--')
    else:
        ax.plot([0, 1, 2, 3, 4, 5], 'o--')


def get3dFigure():
    """
    获取3d画布

    :return: ax
    """
    # figure
    fig = plt.figure(dpi=64, figsize=(16, 16), clear=True)
    ax = fig.add_subplot(111, projection='3d')
    fig.set_facecolor('#2a5fa6')
    # ax.patch.set_alpha(0.0)
    # plt.tight_layout(pad=-20, w_pad=0, h_pad=0)

    # 设置窗格颜色
    # ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    # ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    # ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))

    # 前3个参数用来调整各坐标轴的缩放比例
    # ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([0.8, 1, 0.5, 1]))

    # set label
    ax.set_xlabel('X', fontsize=10)
    ax.set_ylabel('Y', fontsize=10)
    ax.set_zlabel('Z', fontsize=10)

    return fig, ax


def plotPointCloud(point_cloud):
    """
    绘制点云canvas

    :param point_cloud:
    :return:
    """
    fig, ax = get3dFigure()
    ax.plot3D(*util.split_line(point_cloud, 3), 'o', markersize=1, marker=".")


def plotXYZ(x, y, z, p_size=None):
    """
    绘制点云canvas

    :param x:
    :param y:
    :param z:
    :return:
    """
    global ax
    if ax is None:
        fig, ax = get3dFigure()
    if p_size is None:
        p_size = 1
    ax.plot3D(x, y, z, 'o', markersize=p_size, marker="o")


def plt_show():
    """
    显示绘制

    """
    plt.show()
