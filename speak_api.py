from aip import AipSpeech

import os

APP_ID = '19634084'
API_KEY = 'saX3jh5sr8OWs3skrQXDgPU9'
SECRET_KEY = 'UPg6dGftbCKaQH10ZHMpaSQwOpAa2LOI'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)



def say(word):
    result  = client.synthesis(word, 'zh', 1, {
    'per': 4,
    'vol': 5,
})

    if not isinstance(result, dict):
        with open('./temp/reply.mp3', 'wb') as f:
            f.write(result)
        f.close()
        os.system('play ./temp/reply.mp3')