# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LaptopdealItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Brand = scrapy.Field()
    Model = scrapy.Field()
    Series = scrapy.Field()
    Operating_System = scrapy.Field()
    Screen = scrapy.Field()
    CPU = scrapy.Field()
    Memory = scrapy.Field()
    Storage = scrapy.Field()
    GPU = scrapy.Field()
    GPU_Spec = scrapy.Field()
    DimensionWxDxH = scrapy.Field()
    Weight = scrapy.Field()
    CPU_Type = scrapy.Field()
    CPU_Speed = scrapy.Field()
    Screen_Size = scrapy.Field()
    Touchscreen = scrapy.Field()
    Resolution = scrapy.Field()
    LCD_Features = scrapy.Field()
    Wide_Screen_Support = scrapy.Field()
    SSD = scrapy.Field()
    HDD = scrapy.Field()
    Storage_Spec = scrapy.Field()
    Optical_Drive = scrapy.Field()
    WLAN = scrapy.Field()
    Bluetooth = scrapy.Field()
    USB  = scrapy.Field()
    Video_Port = scrapy.Field()
    HDMI = scrapy.Field()
    Backlit = scrapy.Field()
    Webcam = scrapy.Field()
    Card_Reader = scrapy.Field()
    Style = scrapy.Field()
    Type = scrapy.Field()
    Usage = scrapy.Field()
    AC_Adapter = scrapy.Field()
    Battery = scrapy.Field()
    Price_Current = scrapy.Field()
    Price_Previous = scrapy.Field()
    Refresh_Rate = scrapy.Field()
    Saving = scrapy.Field()
    # review = scrapy.Field()
    # review_num = scrapy.Field()