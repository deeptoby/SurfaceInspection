from ctypes import *
lib = cdll.LoadLibrary('libstructPoint.so')

class structImgTest(Structure):
    _fields_ =[('width', c_int),
               ('height', c_int),
               ('channels', c_int),
               ('buf', POINTER(c_ubyte))]


def getstructImg(width, height, channels):
    #cwidth = c_int(width)
    #cheight = c_int(height)
    #cchannels = c_int(channels)
    num = width * height * channels
    data_buf = (c_byte * num)()
    for i in range(num):
        data_buf[i] = i

    pbuf = cast(data_buf, POINTER(c_ubyte))

    st = structImgTest(width, height, channels, pbuf)
    return st

#获取函数返回的char *
lib.getSturctureInfo.restype = POINTER(c_ubyte)
info = lib.getSturctureInfo()
print(chr(info[0]))

# 传入getstructImg
st = getstructImg(3, 3, 3)
lib.showStructureInfo(st)

