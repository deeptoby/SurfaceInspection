r"""
与树莓派通讯的相关接口

"""
import requests as req
import simplejson as json

class Connect:
    host = ''
    port = 8080

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.request_prefix = 'http://%s:%s' % (host, port)

    def request(self, url, data):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        res = req.post(('%s%s' % (self.request_prefix, url)), data=json.dumps(data),
                 headers=headers)

        return res
