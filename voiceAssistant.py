import snowboydecoder
import sys
import signal

import os
import datetime
import time
import threading
import rec
import speech_api
import speak_api
import weather
import turing
import settedAnswer
import netCheck

# Demo code for listening to two hotwords at the same time

isWork = False
interrupted = False
netStatus=True

preTime = datetime.datetime.now()
curTime = datetime.datetime.now()

confidenceLevel = 0
confidence = [0, 0.1, 0.2, 0.3, 0, 4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

class checkNet (threading.Thread):
    def run(self):
        global netStatus
        while True:
            netStatus=netCheck.ping_netCheck()
            time.sleep(1)

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        if not checkWork():
            print('out!')
            return
        rec.rec_fun()
        threads.remove(self)
        if not checkWork():
            print('out!')
            return
        result = speech_api.stt()
        if not checkWork():
            print('out!')
            return
        talk(result)
        stop()
        print("退出线程：" + self.name)


def changeConfidence():
    global preTime
    global curTime
    global confidenceLevel

    if abs(curTime.minute-preTime.minute) <= 1 \
        and curTime.day == preTime.day \
        and curTime.month == preTime.month \
        and curTime.year == preTime.year:
        if confidenceLevel < 10:
            confidenceLevel += 1
    else:
        if confidenceLevel > 0:
            confidenceLevel -= 1


def start():
    global isWork
    global netStatus
    if not isWork:
        if netStatus:
            isWork = True
            print('called')
            m = myThread(1, 'Hello', 1)
            m.setDaemon(True)
            threads.append(m)
            os.system('play ./resources/ding.wav')
            m.start()
        else:
            os.system('play ./resources/netError.mp3')


def stop():
    global isWork
    isWork = False


def cancel():
    stop()
    speak_api.say('好的')


def checkWork():
    global isWork
    return isWork


def talk(word):
    print(word)
    reply=settedAnswer.getAnswer(word)
    if not reply == '':
        speak_api.say(reply)
    elif '今天天气' in word:
        reply = weather.moji()
        speak_api.say(reply)
    else:
        global curTime
        curTime=datetime.datetime.now()
        changeConfidence()
        eg_question = {'text': word, 'confidence': confidence[confidenceLevel]}
        reply = turing.chat(eg_question)
        speak_api.say(reply)


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


if len(sys.argv) != 3:
    print("Error: need to specify 2 model names")
    print("Usage: python demo.py 1st.model 2nd.model")
    sys.exit(-1)

threads = []
models = sys.argv[1:]

monitorNet= checkNet()
monitorNet.start()

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.5]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
callbacks = [lambda: start(),
             lambda: cancel()]
print('Listening... Press Ctrl+C to exit')

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
