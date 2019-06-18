import requests
from bs4 import BeautifulSoup
import re

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit'
                      '/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                      'i/537.36',
    }

def baidu(key):
    res = requests.get('https://baike.baidu.com/item/'+str(key), headers=headers)
    res.encoding = 'utf-8'
    # get info by BeautifulSoup
    soup = BeautifulSoup(res.text, "html.parser")
    try:
        temp = soup.find('div', attrs={'class': 'lemma-summary'}).find('div', attrs={'class': 'para'}).getText()
        # clear the reference tag
        if '[' in temp:
            result = re.findall(r"\[(.*)\]",temp)
            for i in result:
                temp=temp.replace('['+i+']','')     
        temp=temp.replace('\n','')
    except:
        return('未找到结果')
    print(temp)
    return temp

def get(word):
    key=re.search(r'搜索.*',word).group(0)
    key=key[2:]
    return baidu(key)

if __name__ == '__main__':
    get('我要搜索忆江南')
