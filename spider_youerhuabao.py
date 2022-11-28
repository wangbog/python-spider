#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
幼儿画报 - 金龟子讲睡前故事

@author: tony626
"""

from urllib.request import urlopen, Request
import urllib.request
import json
import pandas as pd
import os

ALBUM_ID = '1501661394029625348'  # album_id
TIME_OUT = 10
DOWNLOAD_DIR = '/Users/tony626/Downloads/temp'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
urlAlbum = 'https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIxODEwNjg0MA==&action=getalbum&album_id=ALBUM_ID&count=10&f=json'
urlAlbum = urlAlbum.replace('ALBUM_ID', ALBUM_ID)

# 2=init(first time), 1=continue(return from appmsgalbum api)
continue_flag = 2
url = urlAlbum
while (continue_flag > 0):
    print('url: ' + url)
    reqAlbum = Request(url, headers=headers)
    contentAlbum = urlopen(reqAlbum, timeout=TIME_OUT).read()
    dataAlbum = pd.DataFrame(json.loads(contentAlbum))
    continue_flag = int(dataAlbum['getalbum_resp']['continue_flag'])
    dataAlbum = dataAlbum['getalbum_resp']['article_list']
    dataAlbum = pd.DataFrame(dataAlbum)[
        ['pos_num', 'title', 'url', 'msgid', 'itemidx']]
    print('dataAlbum: ' + dataAlbum)
    msgid = dataAlbum.iloc[-1]['msgid']
    itemidx = dataAlbum.iloc[-1]['itemidx']
    url = urlAlbum + '&begin_msgid=' + msgid + '&begin_itemidx=' + itemidx

    for index, row in dataAlbum.iterrows():
        posArticle = row['pos_num']
        titleArticle = row['title']
        filepath = DOWNLOAD_DIR + '/' + posArticle + '.' + titleArticle + '.mp3'
        print('filepath: ' + filepath)

        if not (os.path.exists(filepath)):
            urlArticle = row['url']
            urlArticle = urlArticle.replace('?', '?f=json&')
            print('urlArticle: ' + urlArticle)
            reqArticle = Request(urlArticle, headers=headers)
            contentArticle = urlopen(reqArticle, timeout=TIME_OUT).read()
            dataArticle = json.loads(contentArticle)
            if(len(dataArticle['voice_in_appmsg']) > 0):
                urlVoice = 'https://res.wx.qq.com/voice/getvoice?mediaid=' + \
                    dataArticle['voice_in_appmsg'][0]['voice_id']
                print('urlVoice: ' + urlVoice)
                urllib.request.urlretrieve(urlVoice, filepath)

print('!!!!work done!!!!')
