import requests
import execjs
from urllib.parse import unquote,quote,urlencode
import json
import codecs

class CloudMusic():
    def __init__(self,name):
        self.name=name
        self.e='010001'
        self.f='00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.g='0CoJUm6Qyw8W8jud'
    def get_data(self,d):
        self.d =d
        with open('js_content2.js', encoding='utf-8')as f:
            JS = f.read()
        data_ = execjs.compile(JS).call('d', self.d, self.g)
        self.i=data_['A'][::-1]
        data={
            'params': data_['encText'],
            'encSecKey': format(int(codecs.encode(self.i.encode('utf-8'), 'hex_codec'), 16) ** int(self.e, 16) % int(self.f, 16), 'x').zfill(256)
        }
        return data
    def  get_id(self):
        url='https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        headers={
            'Referer':'https://music.163.com/search/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        d='{hlpretag:"<span class = \'s-fc7\'>",hlposttag:"</span>",s:"%s",type:"1",csrf_token:"",total:"true",offset:"0"}'%self.name
        response=json.loads(requests.post(url=url,headers=headers,data=self.get_data(d)).content.decode('utf-8'))['result']['songs']
        return [x['id'] for x in response],list(map(lambda x:['网易云',x['name'],'/'.join([i['name'] for i in x['ar']])],response))
    def sprider(self):
        IDs,informations=self.get_id()
        for ID,information in zip(IDs,informations):
            url='https://music.163.com/weapi/song/enhance/player/url?csrf_token='
            headers={
                'Referer':'https://music.163.com/',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
            }
            d=str({'ids':"[%s]"%str(ID),'br':320000,'csrf_token':""})
            response = json.loads(requests.post(url=url, headers=headers, data=self.get_data(d)).content.decode('utf-8'))['data'][0]['url']
            if response!='':
                information.append(response)
            else:
                information.append('-'*180)
        return informations

a = CloudMusic('夜空中最亮的星')
b = a.sprider()
print(b)