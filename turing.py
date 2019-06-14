import json
import urllib.request


def chat(question):
    api_url = "http://openapi.tuling123.com/openapi/api/v2"
    text_input = question['text']
    req = {
        "perception":
            {
                "inputText":
                    {
                        "text": text_input
                    },

                "selfInfo":
                    {
                        "location":
                            {
                                "city": "上海",
                                "province": "上海",
                                "street": "文汇路"
                            }
                    }
            },

        "userInfo":
            {
                "apiKey": "1f151ecec9fa4e219e67b20ad3669d2b",
                "userId": "userId"
            }
    }
    # 将字典格式的req转为utf8编码的字符串
    req = json.dumps(req).encode('utf8')

    print('\n' + '正在调用图灵机器人API...')
    http_post = urllib.request.Request(api_url, data=req, headers={
                                       'content-type': 'application/json'})
    response = urllib.request.urlopen(http_post)

    print('得到回答，输出为字典格式：')
    response_str = response.read().decode('utf8')
    response_dic = json.loads(response_str)
    intent_code = response_dic['intent']['code']

    # 返回网页类的输出方式
    if (intent_code == 10023):
        results_url = response_dic['results'][0]['values']['url']
        results_text = response_dic['results'][1]['values']['text']
        answer = {"code": intent_code,
                  "text": results_text, "url": results_url}
        print(answer)
        return (answer)
    # 一般的输出方式
    else:
        answer = response_dic['results'][0]['values']['text']
        print(answer)
        return answer


if __name__ == '__main__':
    eg_question = {'text': '你好吗', 'confidence': 0.9}
    chat(eg_question)
