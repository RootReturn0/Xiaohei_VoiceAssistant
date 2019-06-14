answerList = {
    'none': '我听不清，你能再说一遍吗',
    'name': '我一直都叫小黑',
    'teacher': '我的老师是沈莹老师，她是我最喜欢的老师',
    'favorite': '她特别好，我喜欢她'
}


def getAnswer(word):
    if word == '':
        return answerList['none']
    if word == '你是谁' \
        or ('你叫什么' in word) \
        or word == '你的名字' \
        or word == '名字' \
        or (('你的名字' in word) and ('什么' in word)):
        return answerList['name']
    if '你的老师' in word:
        return answerList['teacher']
    if '沈莹' in word:
        return answerList['favorite']

    return ''
