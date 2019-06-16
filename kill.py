import os
import psutil
import signal


def killSox():
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == 'sox': # Raspberry Pi 'play'; macOS 'sox'
            print('sox '+str(pid))
            os.kill(pid, signal.SIGTERM)
