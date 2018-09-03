# !/usr/bin/python
# -*- encoding: utf-8 -*-
# @author:spider1998

IMAGE_CODE_EXPIRES_SECONDS = 120  #图片验证码有效时间（秒）
SMS_CODE_EXPIRES_SECONDS = 300  #短信验证码有效时间（秒）

AREA_INFO_REDIS_EXPIRES_SECONDS = 86400 #区域信息缓存时间（秒）
REDIS_HOUSE_INFO_EXPIRES_SECONDES = 86400 # redis缓存房屋信息的有效期

HOME_PAGE_MAX_HOUSES = 5 # 主页房屋展示最大数量
HOME_PAGE_DATA_REDIS_EXPIRE_SECOND = 7200 # 主页缓存数据过期时间 秒

HOUSE_LIST_PAGE_CAPACITY = 3 # 房源列表页每页显示房屋数目
HOUSE_LIST_PAGE_CACHE_NUM = 2 # 房源列表页每次缓存页面数

REDIS_HOUSE_LIST_EXPIRES_SECONDS = 600 # 列表页数据缓存时间 秒