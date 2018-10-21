#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pyassimp import *
import numpy as np
import math
import copy

def load_resource(path):
    scene = load(path)
    assert len(scene.meshes)
    mesh = scene.meshes[0]
    assert len(mesh.vertices)

    return scene.meshes


def rotation(meshs, angel, center, where):
    cos = math.cos(angel)
    sin = math.sin(angel)
    for m in meshs:
        for v in m.vertices:
            now = v[where[0]]
            v[where[0]] = (now - center[0]) * cos - (v[where[1]] - center[1]) * sin
            v[where[1]] = (v[where[1]] - center[0]) * cos + (now -center[1]) * sin

def axis_conversion(meshs, angel, p):
    """
    Args:
        meshs: 模型
        angel: [angel1, angel2, angel3]分别对应绕x，绕y，绕z轴旋转
        p: [(y, z), (x, z), (x, y)]绕三个轴上面的中心坐标

    Return: None
    """
    for i in range(len(angel)):
        if i == 0:
            a, b = 1, 2
        elif i == 1:
            a, b= 0, 2
        else:
            a, b = 0, 1
        rotation(meshs, math.radians(angel[i]), p[1], [a, b])

def translation(meshs, vector):
    """
    Args:
        meshs: 模型
        vector: 平移向量

    Return: None
    """
    for m in meshs:
        for v in m.vertices:
            for i in range(3):
                v[i] += vector[i]

def form_data(meshs, camara):
    """
    Args:
        meshs: 网格数据，包含了面和顶点, 并且所有的点都是正数
        camara Camara对象(相机数量，覆盖区域，步长，开始坐标...)

    Return: N*M*K(nodes) 各个相机轨迹上的区域覆盖的所有点, k值可以细分区域
            使得得到的区域中取最大值可以代表他们离相机最近的也就是靠近表面
            的面的平均值，当前K取1。
    """
    n = camara.num
    min_x, max_x = 1000, -1000
    min_z, max_z = 1000, -1000
    min_y, max_y = 1000, -1000

    for m in  meshs:
        for v in m.vertices:
            min_x = min(min_x, v[0])
            max_x = max(max_x, v[0])
            min_z = min(min_z, v[2])
            max_z = max(max_z, v[2])
            min_y = min(min_y, v[1])
            max_y = max(max_y, v[1])

    # assert min_z != camara.start_position[2]
    # assert min_x != camara.start_position[0]

    length = max_x - min_x
    c_nums = math.ceil((length - camara.over_length) /
                       (camara.width - camara.over_length))

    cells = [[[] for j in range(c_nums)] for i in range(n)]

    for m in meshs:
        for v in m.vertices:
            i = math.ceil((v[1] - min_y) / camara.height)
            if i > n:
                continue
            i = i -1
            j =  math.ceil((v[0] - min_x) / camara.width)
            if j > c_nums:
                continue
            j = j -1

            cells[i][j].append([v[0], v[1], v[2]])

    return cells

def get_trace(cells, camara):
    cells = np.array(cells)
    cells_min = np.abs(cells[:, :, :, 1] - camara._start_position[1]).min(1)
    return cells_min.resize(cells.shape[0], -1)
