#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import threading
import math
# import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BOARD)

__all__ = ['Motor', 'Controller']

class Motor(object):
    """ 电机的相关参数，和操作。

    """
    CYCLE_STEPS = 800  # 800个脉冲
    LENGTH = 4 * 1000  # 微米

    UNIT_DISTANCE_M = 1  # 单位脉冲
    UNIT_DISTANCE_G = 5  # 微米

    FREQUENCY = 800

    name = ''
    io_pwm, io_direction = None, None

    flag_status = False
    pulse_accumulation = 0
    position = 0.0
    action_time = 0.0

    lock = threading.Lock()

    def __init__(self, name, pi_pulse_port, pi_direction_port):
        # self.io_direction = pi_direction_port
        # GPIO.setup(pi_direction_port, GPIO.OUT)
        # GPIO.setup(pi_pulse_port, GPIO.OUT)
        #
        # self.io_pwm = GPIO.PWM(pi_pulse_port, self.FREQUENCY)

        self.name = name

    def get_action_time(self, pulse_number):
        return pulse_number * (self.CYCLE_STEPS / self.FREQUENCY)

    def get_pulse_number(distance):
        if distance % 5 == 0:
            return int(distance / 5)
        elif distance % 5 > 2.5:
            return math.ceil(distance / 5)
        else:
            return math.floor(distance / 5)

    def action_handle(self, index, direction, action_time):
        GPIO.outpu(self.pi_direction_port[index], direction)
        self.PWM[index].start(1)
        time.sleep(action_time / 1000)
        self.PWM[index].stop()
        self.lock.acquire()
        self.shaft_status[index] = False
        self.lock.release()

    def action(self, shaft_index, direction, distance):
        self.lock.acquire()
        if self.flag_status:
            self.lock.release()
            return False, 'aready run'

        self.flag_status = True
        self.lock.release()

        pulse_number = self.get_pulse_number(distance)
        action_time = self.get_action_time(pulse_number)
        if direction == 1:
            self.pulse_accumulation += pulse_number
            self.position += distance
            self.action_time += action_time
        else:
            self.pulse_accumulation -= pulse_number
            self.position -= distance
            self.action_time -= action_time

        threading.Thread(target=self.action_handle,
                         args=(shaft_index, direction, action_time)).start()

        return True, 'run success'

    def zero(self, shaft_index):
        threading.Thread(target=self.action_handle,
                         args=(self.action_time > 0, self.action_time)).start()
    def error_correction(self):
        pass


class Controller(object):
    """ 控制器，最重要的功能是控制当前电机的协作。

    Args:
        nums：电机数量
        motors: 电机实例
        trace: 路劲规划序列，每一序列是由所有电机序列构成的，执行完一个序列
               是指trace中的一个序列。
    """

    nums = 0
    motors = []

    trace = []
    flag_motors_status = []
    flag_trace_status = False

    # 相机的开关
    camara_ports = []

    lock = threading.Lock()

    def __init__(self, motors, camara_ports):
        self.motors = motors
        self.nums = len(motors)
        self.flag_trace_status = [False for i in range(self.nums)]
        if self.nums <= 0:
            raise RuntimeError('电机数量不应该小于1')

    def take_pictures(self):
        print('take pictures')

    def load_trace(self, trace):
        self.lock.acquire()
        if self.flag_trace_status:
            return False, '正在执行该路径'
        self.flag_trace_status = False
        self.trace = trace
        self.lock.release()

    def release_trace(self):
        self.flag_trace_status = False
        self.trace = []

    def trace_action_valide(self):
        for j in self.flag_motors_status:
            if j:
                return False
        return True

    def perform_trace(self):
        def callback(index):
            flag_motors_status = self.flag_motors_status
            def change_status():
                flag_motors_status[index] = not flag_motors_status[index]
            return change_status

        for t in self.trace:
            while not self.trace_action_valide():
                pass
            if self.t['type'] == 'takepictures':
                self.take_pictures()
            elif self.t['type'] == 'move':
                for tt in t['trace']:
                    self.motors[tt['index']].\
                        action(tt['direction'], tt['distance'],
                               callback(tt['index']))


