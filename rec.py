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
    
    print("recording...")

    frames = []
    # if time > 0:
    #     for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #         data = stream.read(CHUNK)
    #         frames.append(data)
    
    startF = 0
    endF = 0
    threshold=5000
    while True:
        data = stream.read(CHUNK)
        chunkData = np.frombuffer(data, np.dtype('<i2'))
        # print(rt_data*10)
        # Fast Fourier Transform
        fftTempData = fftpack.fft(chunkData, chunkData.size, overwrite_x=True)
        fftData = np.abs(fftTempData)[0:fftTempData.size // 2 + 1]

        # test threshold to find a better one
        print('mic: ',sum(fftData) // len(fftData))

        # check if the user stoped speaking by threshold
        if sum(fftData) // len(fftData) > threshold:
            startF += 1
        else:
            endF += 1
        oneSecond=int(RATE / CHUNK) # the number of chunks in one second
        if endF + startF > oneSecond * 1.5:  # Say nothing after being waked up more than 1.5s
            if endF > oneSecond:  # Say nothing after saying somthing more than 1s
                break
            else:
                endF = 0
                startF = 0
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
