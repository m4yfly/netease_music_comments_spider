# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class CommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    songId = Field()
    songName = Field()
    nickname = Field()
    beRepliedContent = Field()
    time = Field()
    content = Field()

    def get_insert_sql(self):
        insert_sql = """
                call add_uniq_music_163_com_comments(%s, %s, %s, %s, %s, %s)
                """
        params = (
                    self["songId"],self["songName"],self["nickname"],self["beRepliedContent"],self["time"],
                    self["content"]
                )
        return insert_sql,params
