## Usage

(听到“叮”代表唤醒词已识别，接下来执行五秒录音；启动监听唤醒词为“嘿小黑”，取消正在执行的任务为“小黑取消”)

### macOS

`python3 voiceAssistant.py hixiaohei.pmdl xiaoheiquxiao.pmdl`

### Windows

`python voiceAssistant.py hixiaohei.pmdl xiaoheiquxiao.pmdl`

**The version of Python must be 3.x**

## Dependencies

### sox

(播放文件用的，如果其他方式播放音频文件，可以在speak_api里改）

### portaudio

#### macOS

`brew install portaudio`

#### linux(Debian)

`sudo apt-get install portaudio`

### pyAudio

`pip3 install pyaudio`

### baidu-aip

`pip3 install baidu-aip`

### wave

`pip3 install wave`

### BeautifulSoup

`pip3 install beautifulsoup4`

(在墨迹爬天气用的，目前只能爬今天的，也并不打算加其他日期的。。。)