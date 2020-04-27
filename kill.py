import os
import psutil
import signal


def killSox():
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == 'play': # Raspberry Pi 'play'; macOS 'play'('sox' in v10.14)
            print('play '+str(pid))
            os.kill(pid, signal.SIGTERM)
