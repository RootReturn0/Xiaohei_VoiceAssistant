# Voice Assistant

*This project only support Chinese for now.*

**This project does not support Windows platform!**

This project is to make a voice assistant whose name is Xiaohei for your own, which can chat and search some knowledge in Baidu Baike .

## Usage

`python3 voiceAssistant.py hixiaohei.pmdl xiaoheibizui.pmdl xiaoheiquxiao.pmdl`

The sound "Dong" means Xiaohei is ready, you can start to talk with Xiaohei.. 

### Hotword

* You should say "嘿小黑"*(hei xiao hei)* to wake Xiaohei up everytime you would like to say something to it. After you hear the sound "Ding", Xiaohei will be awake.
* You can say "小黑闭嘴"*(xiao hei bi zui)* to make Xiaohei shut up.
* You can say "小黑取消"*(xiao hei qu xiao)* to cancel the task you ask Xiaohei to do, such as search.

### What Xiaohei can do

* Translate the English word you said. *You should say and only say one single English word!*
* Tell you some information when you say "搜索xxx". The key word for search is the content you said after saying "搜索".
* Chat with you whatever you say to it.


## Dependencies

**Language: Python3.x**

### sox

#### macOS

`brew install sox`

#### Linux(Debian)

`sudo apt-get install sox`

`sudo apt-get install sox-fmt-all`

### portaudio

#### macOS

`brew install portaudio`

#### Linux(Debian)

`sudo apt-get install portaudio-dev`

### snowboy

go to [snowboy](https://github.com/Kitt-AI/snowboy) by KITT.AI for detail

### baidu-aip

`pip3 install baidu-aip`

### pyAudio

`pip3 install pyaudio`

### wave

`pip3 install wave`

### BeautifulSoup

`pip3 install beautifulsoup4`

### requests

`pip3 install requests`

### psutil

`pip3 install psutil`

### numpy

`pip3 install numpy`

You'd better use `sudo apt-get install python3-numpy` in Raspberry Pi.

### scipy

`pip3 install scipy`

You'd better use `sudo apt-get install python3-scipy` in Raspberry Pi.