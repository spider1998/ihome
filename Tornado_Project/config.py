# !/usr/bin/python
# -*- encoding: utf-8 -*-
# @author:spider1998
import os

#Application配置参数
settings = {
    "static_path":os.path.join(os.path.dirname(__file__),"static"),
    "template_path":os.path.join(os.path.dirname(__file__),"template"),
    "cookie_secret":"A2tpF8hMRsaFozzANLTWH4ZaAncsAE2BvX3gSGgLkiE=",
    'login_url':'/login',
    "xsrf_cookies":True,
    "debug":True,

}

#mysql
mysql_options = dict(
    host="127.0.0.1",
    database="ihome",
    user="root",
    password="123456"
)

#redis
redis_options = dict(
    host="127.0.0.1",
    port="6379"
)

#tail -f log
log_file = os.path.join(os.path.dirname(__file__),"logs/log")
log_level = "debug"

session_expires = 86400 #sesion数据有效期(秒)

passwd_hash_key = "ihome@$^*"

image_url_prefix = "http://pe7u12mgt.bkt.clouddn.com/"
