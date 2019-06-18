#!/usr/bin/python

import os
import time
import win32gui
import win32api
import win32con
import pymouse, pykeyboard
import win32ui
from pymouse import *
from pykeyboard import PyKeyboard
from ctypes import *
import pyHook
import win32com
import pythoncom
import subprocess

from wxpy import embed


def Start(pwd):
    # 打开360Connect
    p = subprocess.Popen(args=["C:\Program Files (x86)\Gateway\SSLVPN\gwclient.exe"])

    time.sleep(2)
    # 获取360的窗口句柄
    # 参数1是类名,参数2是360软件的标题
    a = win32gui.FindWindow(None, "360Connect")
    #返回窗口的显示状态以及被恢复的、最大化的和最小化的窗口位置
    loginid = win32gui.GetWindowPlacement(a)
    print(loginid)
    #返回窗口左上角离显示屏的左上角横向差值
    print(loginid[4][0])
    # 返回窗口左上角离显示屏的左上角纵向差值
    print(loginid[4][1])
    # 定义一个键盘对象
    k = PyKeyboard()
    # 设置鼠标位置,横坐标等于左上角数加输入框离左边界的差值，纵坐标等于左上角数加输入框离上边界的差值
    # 差值可用截图工具，测量像素差值
    windll.user32.SetCursorPos(loginid[4][0]+48, loginid[4][1]+356)
    #模拟鼠标点击操作
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # press mouse
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  # release mouse

    time.sleep(2)
    # 输入密码
    r = str(pwd)
    k.type_string(r)

    time.sleep(2)
    # 按下回车，回车键对应asc码是13926587926587
    win32api.keybd_event(13, 0, 0, 0)
    win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)

    # time.sleep(5)
    # w = win32ui.FindWindow(None,"错误")
    # h = w.GetDlgItemText(0)  # 获得弹窗里的消息文字
    # print(h)
    # buffer = '0' * 50
    # if "错误" in r:
    #     print("动态密码错误")
    #     # 重新执行host_auth.py


if __name__ == "__main__":
        Start(926587)





