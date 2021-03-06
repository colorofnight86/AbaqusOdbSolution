# -*- coding: utf-8 -*-
# @Time    : 2021/11/4 10:10
# @Author  : ColorOfNight
# @Email   : 852477089@qq.com
# @File    : extract_data_from_inp.py
# @Software: PyCharm
# @Description: 提取inp文件中的点和单元

if __name__ == '__main__':
    path = 'E:/new/gongguan/data/'
    file = 'Job-1C1Ddeformed.inp'
    node = 'target_node.csv'
    element = 'target_element.csv'

    with open(path+file, 'r') as fr, open(path+node, 'w+') as fw_node, open(path+element, 'w+') as fw_element:
        content = fr.readline()
        while content[0:5] != '*Node':
            content = fr.readline()
        content = fr.readline()
        # node
        while content[0:8] != '*Element':
            fw_node.write(content.replace(' ', ''))
            content = fr.readline()
        content = fr.readline()
        # element
        while content[0:5] != '*Nset':
            fw_element.write(content.replace(' ', ''))
            content = fr.readline()


