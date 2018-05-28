# -*- coding: utf-8 -*-
import scrapy
from netease_music_comments_spider.items import CommentItem
from scrapy.loader import ItemLoader
import json
from scrapy.http import Request
from urllib import parse
from datetime import datetime
from scrapy.http import FormRequest

def change_datetime_163music(_value):
    time = datetime.fromtimestamp(_value/1000)
    return time.strftime('%Y-%m-%d %H:%M:%S')

class Music163CommentsSpider(scrapy.Spider):

    name = 'music_163_comments'
    allowed_domains = ['music.163.com']

    def __init__(self,nickname=None,*arg,**kwargs):
        super(Music163CommentsSpider,self).__init__(*arg,**kwargs)
        self.nickname = nickname

    def start_requests(self):
        url = 'http://music.163.com/api/cloudsearch/get/web'
        if self.nickname:
            yield FormRequest(
                url = url,
                formdata = {'s':self.nickname,'type':'1002','limit':'1'},
                callback = self.parse_user
            )
        else:
            print("Please follow this: scrapy crawl music_163_comments -a nickname=yournickname")

    def parse_user(self,response):
        try:
            users = json.loads(response.body)['result']['userprofiles']
            if(users):
                userId = str(users[0]['userId'])
                # 此处只处理了前100个歌单
                yield FormRequest(
                    url = 'http://music.163.com/api/user/playlist',
                    formdata = {'uid':userId,'offset':'0','limit':'100'},
                    callback = self.parse_playlist
                )
            else:
                print("cant find the user")
        except Exception as e:
            print("parse_user exception:",e)
    
    def parse_playlist(self,response):
        try:
            playlists = json.loads(response.body)['playlist']
            # print("id:",playlists[0]['id'])
            for item in playlists:
                url = 'http://music.163.com/playlist?id=' + str(item['id'])
                yield Request(url,callback=self.parse_song)
        except Exception as e:
             print("parse_playlist exception:",e)

    def parse_song(self, response):
        songSelector = response.xpath('//a[re:test(@href, "/song\?id=\d+")]')
        for song in songSelector:
            songName = song.xpath('text()').extract_first()
            songId = song.xpath('@href').re('\d+')[0]
            url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_' + songId + "?limit=100&offset=0"
            yield Request(url,meta={"songId":songId,"songName":songName},callback=self.parse_comment)

    def parse_comment(self,response):
        try:
            allComments = json.loads(response.body)
            comments = allComments['comments']
            total = allComments['total']
            songId = response.meta['songId']
            songName = response.meta['songName']
            if(comments):
                for userComment in comments:

                    item = CommentItem()
                    item['nickname'] = userComment['user']['nickname']
                    item['time'] = change_datetime_163music(userComment['time'])
                    repliedUser = userComment['beReplied']
                    if(repliedUser):
                        item['beRepliedContent'] = repliedUser[0]['content']
                    else:
                        item['beRepliedContent'] = ''
                    item['content'] = userComment['content']
                    item['songId'] = songId
                    item['songName'] = songName
                
                    yield item

                paramsStr = response.url.split('?')[1]
                params = parse.parse_qs(paramsStr)
                offset = int(params['offset'][0]) + 100
                url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_' + songId + "?limit=100&offset=" + str(offset)
                # 因为有的歌曲offset会不停增长，一直返回最后一页的内容,确保能查到最后一条记录，所以+100
                if offset < total + 100:
                    yield Request(url,meta={"songId":songId,"songName":songName},callback=self.parse_comment)
        except Exception as e:
            print("parse_comment exception:",e)