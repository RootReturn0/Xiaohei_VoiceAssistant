import pyaudio
import wave
import os
import sys

import numpy as np
from scipy import fftpack

def rec_fun():
    print('I am Schrodinger‘s cat!')

    # os.close(sys.stderr.fileno())
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "./temp/command.wav"
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    print("录音中...")

    frames = []
    # if time > 0:
    #     for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #         data = stream.read(CHUNK)
    #         frames.append(data)
    
    stopflag = 0
    stopflag2 = 0
    threshold=3000
    while True:
        data = stream.read(CHUNK)
        rt_data = np.frombuffer(data, np.dtype('<i2'))
        # print(rt_data*10)
        # 快速傅里叶变换
        fft_temp_data = fftpack.fft(rt_data, rt_data.size, overwrite_x=True)
        fft_data = np.abs(fft_temp_data)[0:fft_temp_data.size // 2 + 1]

        # 测试阈值，输出值用来判断阈值
        print('mic: ',sum(fft_data) // len(fft_data))

        # 判断麦克风是否停止，判断说话是否结束，# 麦克风阈值
        if sum(fft_data) // len(fft_data) > threshold:
            stopflag += 1
        else:
            stopflag2 += 1
        oneSecond=int(RATE / CHUNK) # 一秒内块的数量
        if stopflag2 + stopflag > oneSecond * 1.5:  # 主要是唤醒后是否长时间未说话
            if stopflag2 > oneSecond:
                break
            else:
                stopflag2 = 0
                stopflag = 0
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(1)
    # Returns the size (in bytes) for the specified sample format.
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print('end')


if __name__ == '__main__':
    rec_fun()
