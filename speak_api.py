from aip import AipSpeech

import os

APP_ID = '16482077'
API_KEY = 'CgmfcSPiM5YvNjEopovyU2wC'
SECRET_KEY = 'nL5mTrD9djYP6qy0gkNSY0zRzR5M2O2g'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)



def say(word):
    result  = client.synthesis(word, 'zh', 1, {
    'per': 4,
    'vol': 5,
})

    if not isinstance(result, dict):
        with open('./reply.mp3', 'wb') as f:
            f.write(result)
        f.close()
        os.system('play ./reply.mp3')