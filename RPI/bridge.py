r"""
我们采用web请求的方式来控制树莓派的相关操作
init 表示初始化(初始化电机，初始化)
login 用于用户登录，权限控制
index 表示控制器状态查询
start 表示开始trace
load_trace 表示加载trace
"""

import sys
import web
import simplejson as json
from RPI.controller import Motor, Controller

urls = (
    '/', 'index',
    '/login', 'login',
    '/start', 'start',
    '/load_trace', 'loadtrace',
    '/init', 'init'
)

motors = []
controller = None

class Conf:
    def __init__(self):
        web.header('content-type', 'text/json')
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', 'GET, POST')

    def get_json(self):
        data = web.data()
        data = json.loads(data)
        return data

class login:
    def POST(self):
        return ''
class index:
    def GET(self):
        return ''

class start:
    def GET(self):
        controller.perform_trace()
        return ''

class loadtrace(Conf):
    def POST(self):
        data = self.get_json()
        controller.load_trace(data)
        return 'load success'

class init(Conf):
    def POST(self):
        data = self.get_json()
        nums = int(data['nums'])
        for i in range(nums):
            motors.append(Motor(data['names'][i], int(data['pulse'][i]),
                                int(data['direction'][i])))

        controller = Controller(motors)

        return 'init success'

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

