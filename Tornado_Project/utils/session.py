# !/usr/bin/python
# -*- encoding: utf-8 -*-
# @author:spider1998
import uuid
import logging
import json
import config

class Session(object):
    """"""
    def __init__(self,request_handler_obj):
        self._request_handler = request_handler_obj
        self.session_id = request_handler_obj.get_secure_cookie("session_id")
        if not self.session_id:
            #用户第一次访问，生成session_id,全局唯一
            self.session_id = uuid.uuid4().get_hex()
            self.data = {}
        else:
            try:
                data = request_handler_obj.redis.get("sess_%s" % self.session_id)
            except Exception as e:
                logging.error(e)
                self.data = {}
            if not data:
                self.data = {}
            else:
                self.data = json.loads(data)

    def save(self):
        json_data = json.dumps(self.data)
        try:
            self._request_handler.redis.setex("sess_%s" % self.session_id,config.session_expires,json_data)
        except Exception as e:
            logging.error(e)
            raise Exception("save session failed")
        else:
            self._request_handler.set_secure_cookie("session_id",self.session_id)

    def clear(self):
        self._request_handler.clear_cookie("session_id")
        try:
            self._request_handler.redis.delete("sess_%s" % self.session_id)
        except Exception as e:
            logging.error(e)










