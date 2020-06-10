'''
@Author: rootReturn0
@Date: 2020-05-30 00:07:31
@LastEditors: rootReturn0
@LastEditTime: 2020-06-10 23:26:44
@Description: 
'''
from requests_html import HTMLSession
import urllib.request,json
import re
from urllib.parse import quote
import os
import speak_api




def get(word):
    key=re.search(r'播放.*',word).group(0)
    key=key[2:].replace('。','')
    print(key,'?')
    speak_api.say('请稍等！')
    qqmusic = QQ_Music()
    music_list = qqmusic.get_music_list(key)
    songname=qqmusic.download(music_list[0])

    play_mp3(songname)


def play_mp3(songname):
    path="./temp/music/"+songname
    try:
        os.system('play '+path+'.wav')
    except:
        speak_api.say('对不起，没有找到这首歌')


class QQ_Music():
    def __init__(self):
        self.get_music_url='https://c.y.qq.com/soso/fcgi-bin/client_search_cp?new_json=1&remoteplace=txt.yqq.song&t=0&aggr=1&cr=1&w={}&format=json&platform=yqq.json'
        self.get_song_url='https://u.y.qq.com/cgi-bin/musicu.fcg?data={"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"602087500","songmid":["%s"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":24,"cv":0}}'
        self.download_url='http://ws.stream.qqmusic.qq.com/'
        if not os.path.exists("./temp/music"):
            os.mkdir('./temp/music')

    def parse_url(self,url):
        session = HTMLSession()
        response = session.get(url)
        return response.content.decode()

    def get_music_list(self,keyword):
        music_dirt=json.loads(self.parse_url(self.get_music_url.format(quote(keyword))))
        music_list=music_dirt['data']['song']['list']
        # print(music_list)
        song_list=[]
        for music in music_list:
            sing_name=music['singer'][0]['name']
            song_name=music['title_hilight'].replace(r"</em>", "").replace("<em>", "")
            song_list.append({'songmid':music['mid'], 'singer':sing_name,'song_name':song_name})
            # print(str(len(song_list))+'、'+sing_name+'--'+song_name)
        return song_list

    def download(self,song):
        song_dirt = json.loads(self.parse_url(self.get_song_url%song['songmid']))
        download_url = song_dirt["req_0"]["data"]["midurlinfo"][0]["purl"]
        songname=song['song_name']
        print('download_url',download_url)
        if download_url:
            try:
                # 根据音乐url地址，用urllib.request.retrieve直接将远程数据下载到本地
                urllib.request.urlretrieve(self.download_url+download_url, './temp/music/'+songname+ '.m4a')
                print('Successfully Download:' + song['singer']+'--'+song['song_name'] + '.m4a')
                os.system('ffmpeg -i ' +'./temp/music/'+songname+'.m4a ' +'./temp/music/'+songname+'.wav'+' -y')
                os.system('rm -rf '+'./temp/music/'+songname+'.m4a')
                return songname
            except:
                print('Download wrong~')
if __name__ == '__main__':
    get('播放下山')

