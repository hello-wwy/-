import requests
import execjs
import re
from urllib.parse import unquote,quote,urlencode

class WyyMusic():
    """ 定义一些后期需要用到的基本参数，p1-4是获取歌曲的关键中间参数，且经过js调试发现 只有p1是变化的 """
    def __init__(self,song_name):
        self.song_name = song_name   # self代表类的实例。可以表示类中的公共变量
        self.p2 = "010001"
        self.p3 = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.p4 = '0CoJUm6Qyw8W8jud'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3706.400 SLBrowser/10.0.4040.400',
            # 'cookie': '',因为不登录就可以听音乐，说明链接的获取不需要cookie
            # 'Connection': 'close',
            # 'referer': 'https://music.163.com/',
            # 'content-type': 'application/x-www-form-urlencoded',
        }

    def get_info(self):
        """ 获取搜索后所有歌曲的主要信息 """
        url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        p1 = {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "s": "{}".format(self.song_name), "type": "1", "offset": "0","total": "true", "limit": "30", "csrf_token": ""}
        p1 = str(p1)
        res = requests.post(url,headers=self.headers,data=WyyMusic.get_formdata(self,p1)).json()
        songs = res['result']['songs']
        name_list = []
        id_list = []
        singer = []
        for song in songs:
            name_list.append(song['name'])
            singer.append(song['ar'][0]['name'])
            id_list.append(song['id'])
        return name_list,singer,id_list

    def get_formdata(self,p1):
        """获取加密参数，虽然只是调用前端js，但也是程序的核心（而且很多信息都用了encText,encSecKey这两个参数，构造方法完全一样）"""
        with open('js_content.js', 'r', encoding='utf-8') as f:  # 读取js文件
            js_file = f.read()
        js = execjs.compile(js_file)                             # 编译js代码
        res = js.call('d', p1, self.p2, self.p3, self.p4)        # 获取编译后的对象，里面有我们想要的参数
        encText,encSecKey = res['encText'],res['encSecKey']      # 获取链接的最终参数

        data = {
            'params': encText,
            'encSecKey': encSecKey,
        }
        return data

    def get_lyrics(self,id):
        url = 'https://music.163.com/weapi/song/lyric?csrf_token='
        p1 = {"id":"{}".format(id),"lv":-1,"tv":-1,"csrf_token":""}
        p1 = str(p1)
        res = requests.post(url, headers=self.headers, data=WyyMusic.get_formdata(self, p1))
        lrc = res.json()['lrc']['lyric']
        lrc = re.sub(r'[(\d)|(:)|(.)*?]','  ',lrc)
        lrc = re.findall('](.*?)\n',lrc,re.S)
        f = open('1.txt','w',encoding='utf-8')
        for x in lrc:
            if x!='':
                f.write(x)
                f.write('\n')
        return lrc

    def get_song(self, id):
        """获取音乐链接"""
        url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
        p1 = {"ids": "[{}]".format(id), "level": "standard", "encodeType": "aac", "csrf_token": ""}
        p1 = str(p1)
        res = requests.post(url, headers=self.headers, data=WyyMusic.get_formdata(self,p1))
        res_dict = res.json()  # 获取返回的json文件
        song_link = res_dict['data'][0]['url']
        try:
            # song = requests.get(song_link,headers=self.headers).content
            return song_link
        except:
            pass

if __name__ == '__main__':
    print('输入要查询的音乐名：',end='')
    q = input()
    a = WyyMusic('{}'.format(q))
    names = a.get_info()
    # id = a.get_info()
    ids = a.get_info()[2]
    # print(a.get_info()[0])
    for id in ids:
        print(id,end=' ')
    b = a.get_lyrics(ids[0])
    print('\n歌词：')
    print(b)
    for id in ids:
        res = a.get_song(id)
        print(res)