from odbAccess import *
from abaqusConstants import *
import sys
import os

path = 'E:/new/gongguan/data/'
file_name = '20211025-2.odb'
odb = openOdb(path=path + file_name)
step = 'Step-124'
suffix = '.csv'

# 点集和单元集
weld_elements = odb.rootAssembly.instances['WELD_SIMPLIFIED-1'].elementSets['WELD-SOLU']  # 单元集实例
weld_nodes = odb.rootAssembly.nodeSets['WELD-VOLU'].instances[0]  # 点集实例

nodes = odb.rootAssembly.instances['WELD_SIMPLIFIED-1'].nodeSets['WELD-SOLU'].nodes
elements = odb.rootAssembly.instances['WELD_SIMPLIFIED-1'].elementSets['WELD-SOLU'].elements

# 应力 应变(Elements)
ss = ['']*(len(elements)+1)
RF = odb.steps[step].frames[-1].fieldOutputs['S'].getSubset(region=weld_elements).values  # 应力场列表
PQ = odb.steps[step].frames[-1].fieldOutputs['PEEQ'].getSubset(region=weld_nodes).values  # 等效应变列表
PE = odb.steps[step].frames[-1].fieldOutputs['PE'].getSubset(region=weld_nodes).values  # 应变列表
# element参数持久化 elementLabel,PEEQ,PE[6],mises,S11,S22,S33,S12,S13,S23
with open(path + 'strain&stress' + suffix, mode='w+') as f:
    for idx in range(len(PQ)):
        pq = PQ[idx]
        pe = PE[idx]
        rf = RF[idx]
        if pq.elementLabel != pe.elementLabel or pq.elementLabel != rf.elementLabel:
            print('label not equal:', idx)
        ss[pq.elementLabel] = str(pq.elementLabel) + ',' + str(pq.data) + ',' + ','.join(str(i) for i in pe.data) + ',' + str(
            rf.mises) + ',' + ','.join(str(i) for i in rf.data) + '\n'
    for i in range(1, len(elements)+1):
        f.write(ss[i])


# 温度(Nodes)：
temperature = [0.0]*(len(nodes) + 1)
TF = odb.steps[step].frames[-1].fieldOutputs['NT11'].getSubset(region=weld_nodes).values  # 温度场列表
# 节点温度持久化 nodeLabel,temp
with open(path + 'temperature' + suffix, mode='w+') as f:
    for idx in range(len(TF)):
        tf = TF[idx]
        temperature[tf.nodeLabel] = tf.data
    for i in range(1, len(nodes) + 1):
        f.write(str(i) + ',' + str(temperature[i]) + '\n')


# 坐标(Nodes)：
RS = odb.steps[step].frames[-1].fieldOutputs['U'].getSubset(region=weld_nodes).values  # 位移列表
coordinate = ['']*(len(nodes)+1)
coordinate_final = ['']*(len(nodes)+1)
# 点的坐标持久化 nodeLabel,x,y,z
with open(path + 'final_coordinate' + suffix, mode='w+') as f:
    for idx in range(len(nodes)):
        node = nodes[idx]
        rs = RS[idx]
        if node.label != rs.nodeLabel:
            print('label not equal:', idx)
        coordinate_final[node.label] = str(node.label) + ',' + ','.join(
            str(node.coordinates[i] + rs.data[i]) for i in range(len(node.coordinates))) + '\n'
    for i in range(1, len(nodes) + 1):
        f.write(coordinate_final[i])

with open(path + 'coordinate' + suffix, mode='w+') as f:
    for idx in range(len(nodes)):
        node = nodes[idx]
        coordinate[node.label] = str(node.label) + ',' + ','.join(
            str(node.coordinates[i]) for i in range(len(node.coordinates))) + '\n'
    for i in range(1, len(nodes) + 1):
        f.write(coordinate[i])


# 点所属的单元号持久化
nodes = odb.rootAssembly.instances['WELD_SIMPLIFIED-1'].nodeSets['WELD-SOLU'].nodes
elements = odb.rootAssembly.instances['WELD_SIMPLIFIED-1'].elementSets['WELD-SOLU'].elements  # 单元集
nodes_list = [[] for i in range(len(nodes) + 1)]
elements_list = [[] for i in range(len(elements) + 1)]
for element in elements:
    for node_num in element.connectivity:
        elements_list[element.label].append(node_num)
        nodes_list[node_num].append(element.label)

with open(path + 'nodes_info' + suffix, mode='w+') as f:
    for idx in range(1, len(nodes_list)):
        node_list = nodes_list[idx]
        f.write(str(idx) + ',' + ','.join(str(i) for i in node_list) + '\n')

with open(path + 'elements_info' + suffix, mode='w+') as f:
    for idx in range(1, len(elements_list)):
        element_list = elements_list[idx]
        f.write(str(idx) + ',' + ','.join(str(i) for i in element_list) + '\n')








# 指定标签列表获取点集
nodes_test = odb.rootAssembly.instances['WELD_SIMPLIFIED-1'].NodeSetFromNodeLabels('test',
                                                                                   [173, 1548, 1547, 1546, 1545, 1544,
                                                                                    1543, 1542, 2405, 2429, 2453, 2477,
                                                                                    2501, 2525, 2549, 255])
# 点的坐标集（x,y,label）
node_list = [(node.coordinates[0], node.coordinates[1], node.label) for node in nodes_test.nodes]


# 位移
RS = odb.steps[step].frames[-1].fieldOutputs['U'].getSubset(region=nodes_test).values  # 位移列表
rs_list = [(rs.data[0], rs.data[1], rs.nodeLabel) for rs in RS]

# 最后点的坐标，按x排序
lists = [(node_list[i][0] + rs_list[i][0], node_list[i][1] + rs_list[i][1]) for i in range(len(rs_list))]
final_list = sorted(lists, key=lambda x: (x[0]))
