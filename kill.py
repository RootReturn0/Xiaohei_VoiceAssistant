'''
@Author: rootReturn0
@Date: 2019-06-16 13:24:20
@LastEditors: rootReturn0
@LastEditTime: 2020-06-11 00:08:13
@Description: 
'''
import os
import psutil
import signal


def killSox():
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == 'play': # Raspberry Pi 'play'; macOS 'sox'
            print('play '+str(pid))
            os.kill(pid, signal.SIGTERM)
