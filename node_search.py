# -*- coding: utf-8 -*-
# @Time    : 2021/10/29 19:56
# @Author  : ColorOfNight
# @Email   : 852477089@qq.com
# @File    : node_search.py
# @Software: PyCharm
# @Description: 八叉树实现K近邻搜索

import time
import math


class OcTreeNode:
    def __init__(self, idx, boundary, node_contained):
        self.id = idx
        self.boundary = boundary
        self.node_contained = node_contained.copy()
        self.contains_num = len(self.node_contained)


def get_parameter(node_list):
    """
    获取包围边界参数

    :param node_list: 点集
    :return: 包围边界[x,y,z,l]
    """
    k = 1.0 / 1000  # 系数
    x_max, y_max, z_max = node_list[1][0], node_list[1][1], node_list[1][2]
    x_min, y_min, z_min = node_list[1][0], node_list[1][1], node_list[1][2]
    for node in node_list:
        x_max, y_max, z_max = max(x_max, node[0]), max(y_max, node[1]), max(z_max, node[2])
        x_min, y_min, z_min = min(x_min, node[0]), min(y_min, node[1]), min(z_min, node[2])
    length = max(x_max - x_min, y_max - y_min, z_max - z_min)
    return [x_min - k * length, y_min - k * length, z_min - k * length, length * (1 + 2 * k)]


def in_boundary(point, boundary):
    """
    点是否在包围边界里

    :param point: 点坐标[x,y,z]
    :param boundary: 边界大小[x,y,z,l]
    :return: True/False
    """
    l_ = boundary[3]

    return boundary[0] <= point[0] < boundary[0] + l_ and boundary[1] <= point[1] < boundary[1] + l_ and \
        boundary[2] <= point[2] < boundary[2] + l_


def contain_node(node_list, node_index, boundary):
    """
    获取在包围边界里的所有点

    :param node_list: 点集列表[node]
    :param node_index: 候选的点索引[index]
    :param boundary: 边界[x,y,z,l]
    :return: 在边界里的点的索引
    """
    node_contained = []
    for i in node_index:
        if in_boundary(node_list[i], boundary):
            node_contained.append(i)
    return node_contained


def build_octree(node_list, boundary, threshold=12):
    """
    建立八叉树

    :param node_list: 点集
    :param boundary: 初始边界
    :param threshold: 是否继续划分的阈值
    :return: 八叉树节点的字典

    """
    tree = {}
    max_depth = 50
    root = OcTreeNode(0, boundary, [i for i in range(1, len(node_list))])  # 根节点
    tree[0] = root
    build_octree_recursive(node_list, tree, root, 0, max_depth, threshold)
    return tree


def build_octree_recursive(node_list, tree, node, depth, max_depth, threshold):
    """
    递归生成八叉树

    :param node_list: 点集
    :param tree: 八叉树节点的字典
    :param node: 当前节点
    :param depth: 当前深度
    :param max_depth: 最大深度
    :param threshold: 节点阈值
    :return: None
    """
    if depth >= max_depth or node.contains_num < threshold:  # 达到最大深度或者点小于阈值，停止递归
        # print(node.id)
        return
    # 八个子节点
    x, y, z, l_ = node.boundary
    child_boundaries = [[x, y, z, l_ / 2], [x + l_ / 2, y, z, l_ / 2],
                        [x, y + l_ / 2, z, l_ / 2], [x + l_ / 2, y + l_ / 2, z, l_ / 2],
                        [x, y, z + l_ / 2, l_ / 2], [x + l_ / 2, y, z + l_ / 2, l_ / 2],
                        [x, y + l_ / 2, z + l_ / 2, l_ / 2], [x + l_ / 2, y + l_ / 2, z + l_ / 2, l_ / 2]]
    for i in range(8):
        node_contained = contain_node(node_list, node.node_contained, child_boundaries[i])
        child_node = OcTreeNode(node.id * 10 + i + 1, child_boundaries[i], node_contained)
        tree[child_node.id] = child_node
        build_octree_recursive(node_list, tree, child_node, depth + 1, max_depth, threshold)


def load_data(filepath, filename, num=-1, data_type='float'):
    """
    读取数据

    :param filepath: 文件路径
    :param filename: 文件名
    :param data_type: 读取的数据类型
    :param num: 读取数据的个数，<0表示读取全部
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


def tree_info(tree, num, target=-1, threshold=12):
    """
    显示八叉树的信息

    :param tree: 八叉树
    :param num: 点的数量
    :param target: 查找索引为target点的路径
    :param threshold: 划分阈值
    """
    count_array = [0] * (num + 1)
    for key in tree:
        tree_node = tree[key]
        for idx in tree_node.node_contained:
            if 0 < tree_node.contains_num < threshold:
                count_array[idx] += 1
            if 0 < target == idx:  # 查看某节点的路径
                print(key)
    # print('各点的在叶子节点中被包含次数:', count_array)
    tree_list = [key for key in tree]
    # print(tree_list)
    print('\n八叉树总节点数:', len(tree))
    print('最大深度：', len(str(max(tree_list))))


def find_node(tree, point, threshold=12):
    """
    找到八叉树所在的叶子结点

    :param tree: 八叉树
    :param point: 目标节点
    :param threshold: 阈值
    :return: 叶子节点id
    """
    tree_node = tree[0]
    node_id = 0
    if not in_boundary(point, tree[node_id].boundary):
        return node_id
    x, y, z = point[0], point[1], point[2]
    while tree_node.contains_num >= threshold:
        x_, y_, z_, l_ = tree_node.boundary[0], tree_node.boundary[1], tree_node.boundary[2], tree_node.boundary[3]
        child_id = 1
        if z > z_ + l_ / 2:
            child_id += 4
        if y > y_ + l_ / 2:
            child_id += 2
        if x > x_ + l_ / 2:
            child_id += 1
        node_id = node_id * 10 + child_id
        tree_node = tree[node_id]
    if node_id == 0:
        print('find_node未找到目标点的对应节点')
    return node_id


def knn(point_list, tree, points, threshold=12, k=8):
    """
    求点的n个近邻点

    :param point_list: 点集
    :param tree: 八叉树
    :param points: 目标点集
    :param k: 最近邻的点的个数
    :param threshold: 阈值
    :return: 最近邻point的n个点在point_list里的索引
    """
    knn_list = [[]]
    print('\nknn正在生成' + str(k) + '近邻点，数据量：' + str(len(points)) + '/' + str(len(point_list) - 1) + '，阈值：' + str(
        threshold) + '，请稍后……')
    start_time = time.time()
    for point in points:
        node_id = find_node(tree, point, threshold)  # 寻找目标点所在的节点
        knn_point = get_knn(point_list, tree, point, node_id, k)  # 获取每个点的knn
        knn_list.append(knn_point)
    end_time = time.time()
    print('knn耗时：' + str(end_time - start_time) + 's')
    return knn_list


def get_knn(point_list, tree, point, node_id, k):
    """

    :param point_list: 点集
    :param tree: 八叉树
    :param point: 目标点
    :param node_id: 节点id
    :param k: 近邻点数量
    """
    depth = 0
    while True:
        tree_node = tree[node_id]
        if tree_node.contains_num >= 8:
            distance_list = [[idx, distance2(point_list[idx], point)] for idx in tree_node.node_contained]
            sorted_distance = sorted(distance_list, key=lambda x: x[1])  # 按距离从小到大排序
            distance_max = sorted_distance[k - 1][1]
            distance_min = min_distance(point, tree_node.boundary, tree[0].boundary)
            # print(node_id, distance_max <= distance_min, tree_node.node_contained)
            # print(sorted_distance)
            if distance_max <= distance_min or node_id == 0:
                return [pair[0] for pair in sorted_distance[:k]]
        depth += 1
        node_id = int(node_id / 10)


def get_center_point(elements_list, point_list):
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


def min_distance(p, boundary, root_boundary):
    """
    点到边界的最小距离的平方

    :param p: 点(x1,y1,z1)
    :param boundary: 边界(x2,y2,z2,l)
    :param root_boundary: 最外围的边界(x,y,z,l)
    """
    x1, y1, z1 = p[0], p[1], p[2]
    x2, y2, z2, l2 = boundary[0], boundary[1], boundary[2], boundary[3]
    # 优化
    x_min, y_min, z_min = root_boundary[0], root_boundary[1], root_boundary[2]
    x_max, y_max, z_max = root_boundary[0] + root_boundary[3], root_boundary[1] + root_boundary[3], root_boundary[2] + \
        root_boundary[3]
    distances = [root_boundary[3] * root_boundary[3] * 3]
    if x2 > x_min: distances.append((x2 - x1) * (x2 - x1))
    if x2 + l2 < x_max: distances.append((x2 + l2 - x1) * (x2 + l2 - x1))
    if y2 > y_min: distances.append((y2 - y1) * (y2 - y1))
    if y2 + l2 < y_max: distances.append((y2 + l2 - y1) * (y2 + l2 - y1))
    if z2 > z_min: distances.append((z2 - z1) * (z2 - z1))
    if z2 + l2 < z_max: distances.append((z2 + l2 - z1) * (z2 + l2 - z1))
    # 优化前
    # distances = [(x2 - x1) * (x2 - x1), (x2 + l2 - x1) * (x2 + l2 - x1), (y2 - y1) * (y2 - y1),
    #              (y2 + l2 - y1) * (y2 + l2 - y1), (y2 + l2 - y1) * (y2 + l2 - y1),
    #              (z2 - z1) * (z2 - z1), (z2 + l2 - z1) * (z2 + l2 - z1)]
    return min(distances)


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


def get_test(point_list, num=None, n=8):
    """
    生成8个最近邻点的测试集

    :param num: 点的个数
    :param point_list: 点集
    :param n: 近邻点个数
    :return: 测试集
    """
    if not num or num > len(point_list):
        num = len(point_list)
    if num < n:
        return []
    print('\n正在生成' + str(n) + '近邻点测试集，数据量：' + str(num) + '/' + str(len(point_list)) + '，请稍后……')
    start_time = time.time()
    test_list = [[]]
    for i in range(num):
        point1 = point_list[i]
        distance_list = [[j + 1, distance2(point1, point_list[j])] for j in range(len(point_list))]
        sorted_distance = sorted(distance_list, key=lambda x: x[1])  # 按从小到大距离排序
        distance_index = [pair[0] for pair in sorted_distance[:n]]
        test_list.append(distance_index)
    end_time = time.time()
    print('测试集耗时：' + str(end_time - start_time) + 's')
    return test_list


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
    size = len(values[0])
    value = [0.0] * size
    if select == 1:
        distance_list = [distance(point, point2) for point2 in points]
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
        value = [value[j] + values[i][j] * weight for j in range(size)]
    return value


def compare(list1, list2):
    result = []
    for i in range(len(list1)):
        if not list1[i] == list2[i]:
            result.append(i)
    print('\n校验结果：不同的个数为', len(result), result)


def generate_output_file(file_path, nods, els, target_nods, target_els, knn_nods, knn_els, temper_data, stress_data,
                         select):
    start_time = time.time()
    with open(file_path, 'w+') as f:
        # 节点温度生成
        f.write('** PREDEFINED FIELDS\n** \n** Name: Predefined weld-1C1D-temp \
                    Type: STRESS\n*Initial Conditions, type=STRESS\n')
        for target_label in range(1, len(target_nods)):
            target_point = target_nods[target_label]
            knn_labels = knn_nods[target_label]
            f.write(str(target_label) + ', ' +
                    ', '.join(str(el) for el in inverse_distance_weight(target_point, [nods[i] for i in knn_labels],
                                                                        [temper_data[i] for i in knn_labels],
                                                                        select)) + '\n')
        # 单元应力生成
        f.write('\n** Name: Predefined weld-1C1D-temp \
                    Type: Temperature\n*Initial Conditions, type=TEMPERATURE\n')
        for target_label in range(1, len(target_els)):
            target_element = target_els[target_label]
            knn_labels = knn_els[target_label]
            f.write(str(target_label) + ', ' +
                    ', '.join(str(el) for el in inverse_distance_weight(target_element, [els[i] for i in knn_labels],
                                                                        [stress_data[i][1:7] for i in knn_labels],
                                                                        select)) + '\n')
        # 单元应变生成
        f.write('\n** Name: Predefined weld-1C1D-temp \
                    Type: PLASTIC STRAIN\n*Initial Conditions, type=PLASTIC STRAIN\n')
        for target_label in range(1, len(target_els)):
            target_element = target_els[target_label]
            knn_labels = knn_els[target_label]
            f.write(str(target_label) + ', ' +
                    ', '.join(str(el) for el in inverse_distance_weight(target_element, [els[i] for i in knn_labels],
                                                                        [stress_data[i][8:14] for i in knn_labels],
                                                                        select)) + '\n')
        print('\n新模型构建参数文件 input_info.txt 已生成。')
    end_time = time.time()
    print('耗时：' + str(end_time - start_time) + 's')


if __name__ == '__main__':
    # 参数配置
    path = 'E:/new/gongguan/data/'
    node_file = 'final_coordinate.csv'
    element_file = 'elements_info.csv'
    temperature = 'temperature.csv'
    stress = 'strain&stress.csv'
    node_target_file = 'target_node.csv'
    element_target_file = 'target_element.csv'
    output = 'input_info.txt'

    node_num = -1  # 读取点的个数
    target_node_num = -1  # 目标点的个数
    element_num = -1  # 读取单元的个数
    target_element_num = -1  # 目标单元的个数
    max_node_num = 12  # 是否继续划分的阈值

    # 读取数据并生成八叉树
    nodes, node_num = load_data(path, node_file, node_num)  # 已知点集
    elements, element_num = load_data(path, element_file, element_num, data_type='int')  # 已知单元集
    elements = get_center_point(elements, nodes)  # 获取单元的中心点
    print('单元中心点：', elements[:min(20, element_num)], '……' if element_num > 20 else '')
    target_nodes, target_node_num = load_data(path, node_target_file, target_node_num)  # 目标点集
    target_elements, target_element_num = load_data(path, element_target_file, target_element_num,
                                                    data_type='int')  # 目标单元集
    target_elements = get_center_point(target_elements, target_nodes)

    # 节点的八叉树
    parameter_node = get_parameter(nodes[1:])  # 初始参数
    octree_node = build_octree(nodes, parameter_node)  # 生成八叉树
    # tree_info(octree_node, node_num)  # 显示八叉树的相关信息
    # # 单元的八叉树
    parameter_element = get_parameter(elements[1:])
    octree_element = build_octree(elements, parameter_element)
    # tree_info(octree_element, element_num)

    # 获取近邻点
    knn_node = knn(nodes, octree_node, target_nodes[1:])
    # print(knn_node)
    knn_element = knn(elements, octree_element, target_elements[1:])
    # print(knn_element)

    # 生成测试集并验证
    # test_node = get_test(nodes[1:])
    # test_element = get_test(elements[1:])
    # 比较结果
    # compare(knn_node, test_node)
    # compare(knn_element, test_element)

    # 读取温度应力应变数据
    data_temper = load_data(path, temperature, node_num)[0]
    data_stress = load_data(path, stress, node_num)[0]
    #
    # # 生成输出文件
    generate_output_file(path + output, nodes, elements, target_nodes, target_elements,
                         knn_node, knn_element, data_temper, data_stress, 2)
