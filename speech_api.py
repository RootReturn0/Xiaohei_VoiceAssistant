from aip import AipSpeech

APP_ID = '19634084'
API_KEY = 'saX3jh5sr8OWs3skrQXDgPU9'
SECRET_KEY = 'UPg6dGftbCKaQH10ZHMpaSQwOpAa2LOI'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def stt():
    result = client.asr(get_file_content('./temp/command.wav'),
                        'wav',
                        16000,
                        {'dev_pid': 1537, }
                        )
    print(result)

    if result['err_msg'] == 'success.':
        print("I am in")
        word = result['result'][0].encode('utf-8')
        if word != '':
            print("I am really in")
            if word[len(word) - 3:len(word)] == '，':
                word[0:len(word) - 3]
                with open('./temp/command.txt', 'wb') as f:
                    f.write(word[0:len(word) - 3])
                f.close()
            else:
                print(word.decode('utf-8').encode('gbk'))
                with open('./temp/command.txt', 'wb') as f:
                    f.write(word)
                f.close()
        else:
            print("File does not exist or wrong format!")

        return result['result'][0]
    else:
        return ''


if __name__ == '__main__':
    stt()
