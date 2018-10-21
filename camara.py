#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from load_3d import *
import numpy as np

class Camara(object):
    """
    Args:
        _num: 相机数量
        _height: 单个相机覆盖高度
        _widht: 单个相机覆盖宽度
        _step: 按照固定的方向的移动距离
        _start_position: 这里是指相机束开始位置
    """
    _num = 1
    _height = 200
    _width = 200
    _step = 300
    _start_position = None
    _over_length = None
    _distance = None

    def __init__(self, num, height, width, step,
                 start_position, over_length, distance):
        self._num = num
        self._height = height
        self._width = width
        self._step = step
        self._start_position = start_position
        self._over_length = over_length
        self._distance = distance

    def get_trace(self, meshs):
        """
        Args:
            meshs: 车模型的网格数据
        Return:
            N个相机在M个移动方向节点上的坐标。
        """
        cells = form_data(meshs, self)
        n = self.num
        m = len(cells[0])
        trace = [[None for j in range(m)] for i in range(n)]

        for i in range(n):
            for j in range(m):
                arr = np.array(cells[i][j])
                if len(arr) == 0:
                    continue
                trace[i][j] = np.abs(arr[:, 2] - self._start_position[2]).min(0)

        self.cells = cells
        self.trace = trace

    @property
    def num(self):
        return self._num

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def step(self):
        return self._step

    @property
    def start_position(self):
        return self._start_position

    @property
    def over_length(self):
        return self._over_length

    @property
    def distance(self):
        return self._distance