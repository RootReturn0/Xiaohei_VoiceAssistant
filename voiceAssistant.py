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
import baike
import kill

import get_email
import play_music
import reminder
import get_email


isWork = False
interrupted = False
isShutUp = False
netStatus = True

preTime = datetime.datetime.now()
curTime = datetime.datetime.now()

confidenceLevel = 0
confidence = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

detector = ''

def checkWork():
    global isWork
    return isWork


# check the connection of Internet


class checkNet (threading.Thread):
    def run(self):
        while True:
            global netStatus
            netStatus = netCheck.ping_netCheck()
            time.sleep(1)

# check the emails


class checkEmail (threading.Thread):
    def run(self):
        get_email.server_mail()


# Work after being waked


class workThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Start thread：" + self.name)
        if not checkWork():
            print('out!')
            return
        global detector
        detector.terminate()
        rec.rec_fun()
        detector = detectorThread()
        detector.start()
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
        print("Exit thread：" + self.name)


# Change confidence level for Turing Robot.
# Chat more in a short time, it will be more confident.
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

    preTime = curTime

# wake up


def start():
    global isWork
    global netStatus
    if not isWork:
        if netStatus:
            isWork = True
            print('called')
            m = workThread(1, 'Hello', 1)
            m.setDaemon(True)
            threads.append(m)
            os.system('play ./resources/ding.wav')
            m.start()
        else:
            os.system('play ./resources/netError.mp3')

# stop working of current conversation


def stop():
    global isWork
    isWork = False
    kill.killSox()

# shut up


def shutUp(b):
    global isShutUp
    global confidenceLevel

    if not isShutUp:
        isShutUp = True
        stop()
        os.system('play ./resources/ok.mp3')
        if b and confidenceLevel > 0:
            confidence -= 1
        isShutUp = False

# decide what to say


def talk(word):
    print(word)
    reply = settedAnswer.getAnswer(word)
    if not reply == '':
        speak_api.say(reply)
    elif '搜索' in word:
        reply = baike.get(word)
        speak_api.say(reply)
    elif '今天天气' in word:
        reply = weather.moji()
        speak_api.say(reply)
    elif '播放' in word:
        play_music.get(word)
    elif '提醒' in word:
        reminder.get(word)
    else:
        global curTime
        curTime = datetime.datetime.now()
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

class detectorThread (threading.Thread):
    def run(self):
        global detector

        models = ["hixiaohei.pmdl", "xiaoheibizui.pmdl", "xiaoheiquxiao.pmdl"]
        # capture SIGINT signal, e.g., Ctrl+C
        # signal.signal(signal.SIGINT, signal_handler)

        sensitivity = [0.5]*len(models)
        detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
        callbacks = [lambda: start(),
                    lambda: shutUp(False),
                    lambda: shutUp(True)]

        print('Listening...')
        # main loop
        # make sure you have the same numbers of callbacks and models
        detector.start(detected_callback=callbacks,
                interrupt_check=interrupt_callback,
                sleep_time=0.03)

    # Detector.terminate()

if __name__ == '__main__':
    # detector -> Thread -> detector (pyaudio I/O error fixed)

    if len(sys.argv) != 4:
        print("Error: need to specify 3 model names")
        print("Usage: python voiceAssistant.py 1st.model 2nd.model 3rd.model")
        sys.exit(-1)

    threads = []

    monitorNet = checkNet()
    monitorNet.start()

    email = checkEmail()
    email.start()


    os.system('play ./resources/dong.wav')
    detector = detectorThread()
    detector.start()

    
