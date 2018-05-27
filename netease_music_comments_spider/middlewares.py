# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import pymysql
import pymysql.cursors
import random
import requests
from datetime import datetime


class ProxyMiddlewareFromAPI(object):

    def __init__(self,apiUrl=None):
        print("init ProxyMiddlewareFromAPI")
        self.apiUrl = apiUrl
        if apiUrl:
            self.update_proxy_from_api()

    @classmethod
    def from_settings(cls,settings):
        apiUrl = settings["PROXY_API_URL"]
        return cls(apiUrl)    

    def update_proxy_from_api(self):
        self.updateTime = datetime.now()
        res = requests.get(self.apiUrl).content.decode()
        ips = res.split('\n')
        self.ip = 'http://'+ips[0]
    
    def maintain_ip(self):
        timedelta = datetime.now() - self.updateTime
        if timedelta.seconds >= 5:
            self.update_proxy_from_api()
        return self.ip

    def process_request(self,request,spider):
        if self.apiUrl:
            proxy = self.maintain_ip()
            print("this is request ip in request:"+proxy)  
            request.meta['proxy'] = proxy

    def process_response(self,request,response,spider):
        if response.status != 200:
            self.process_request(request,spider)
        elif response.status == 200:
            if(response.xpath('//title/text()').extract() == 'too many request'):
                print('too many request')
                return request
        return response

    def process_exception(self,request, exception, spider):
        return request
