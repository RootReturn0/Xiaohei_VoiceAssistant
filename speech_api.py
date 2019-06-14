from aip import AipSpeech

APP_ID = '16482077'
API_KEY = 'CgmfcSPiM5YvNjEopovyU2wC'
SECRET_KEY = 'nL5mTrD9djYP6qy0gkNSY0zRzR5M2O2g'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def stt():
    result = client.asr(get_file_content('./command.wav'),
                        'wav',
                        16000,
                        {'dev_pid': 1536, }
                        )
    print(result)

    if result['err_msg'] == 'success.':
        print("I am in")
        word = result['result'][0].encode('utf-8')
        if word != '':
            print("I am really in")
            if word[len(word) - 3:len(word)] == '，':
                word[0:len(word) - 3]
                with open('./command.txt', 'wb') as f:
                    f.write(word[0:len(word) - 3])
                f.close()
            else:
                print(word.decode('utf-8').encode('gbk'))
                with open('./command.txt', 'wb') as f:
                    f.write(word)
                f.close()
        else:
            print("音频文件不存在或格式错误")

        return result['result'][0]
    else:
        return ''


if __name__ == '__main__':
    stt()
