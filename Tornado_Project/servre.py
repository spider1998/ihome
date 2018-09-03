# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @author:spider1998
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import config
import torndb
import redis
import logging

from tornado.options import define,options
from tornado.web import RequestHandler
from urls import handlers

define("port",type=int,default=8000,help="run server on the given port")

class Application(tornado.web.Application):
    """"""
    def __init__(self,*args,**kwargs):
        super(Application,self).__init__(*args,**kwargs)
        self.db = torndb.Connection(**config.mysql_options)
        self.redis = redis.StrictRedis(**config.redis_options)

def main():
    options.logging = config.log_level
    options.log_file_prefix = config.log_file
    tornado.options.parse_command_line()
    app = Application(
        handlers,**config.settings
    )
    http_sever = tornado.httpserver.HTTPServer(app)
    http_sever.listen(options.port)
    #http_sever.bind(8000)
    #http_sever.start(0)
    tornado.ioloop.IOLoop.current().start()




if __name__ == '__main__':
    main()