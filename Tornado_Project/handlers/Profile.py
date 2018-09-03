# !/usr/bin/python
# -*- encoding: utf-8 -*-
# @author:spider1998
import logging
import constants
import config

from utils.response_code import RET
from BaseHandler import BaseHandler
from utils.image_storage import storage
from utils.commons import require_logined

class AvatarHandler(BaseHandler):
    """头像"""
    @require_logined
    def post(self):

        user_id = self.session.data["user_id"]

        try:
            avatar = self.request.files["avatar"][0]["body"]
        except Exception as e:
            logging.info(e)
            return self.write(dict(errno=RET.PARAMERR,errmsg="参数出错"))
        try:
            img_name = storage(avatar)
        except Exception as e:
            logging.info(e)
            img_name = None
        if not img_name:
            return self.write({"errno":RET.THIRDERR,"errmsg": "qiniu error"})
        try:
            print "99999"
            self.db.execute_rowcount("update ih_user_profile set up_avatar=%(avatar)s "
                                  "where up_user_id=%(user_id)s",avatar=img_name,user_id=user_id)
        except Exception as e:
            print "____________=====+_____"
            logging.info(e)
            return self.write({"errno":RET.DBERR,"errmsg":"upload failed"})
        img_url = config.image_url_prefix + img_name
        self.write({"errno":RET.OK,"errmsg":"OK","data":img_url})


class ProfileHandler(BaseHandler):
    """个人信息"""
    @require_logined
    def get(self):
        print "********************************************"
        user_id = self.session.data['user_id']

        try:
            ret = self.db.get("select up_name,up_mobile,up_avatar from "
                                  "ih_user_profile where up_user_id=%(up_user_id)s", up_user_id=user_id)
        except Exception as e:
            logging.info(e)
            return self.write({"errno":RET.DBERR, "errmsg":"get data error"})
        if ret["up_avatar"]:
            img_url = config.image_url_prefix + ret["up_avatar"]
        else:
            img_url = None
        self.write({"errno":RET.OK, "errmsg":"OK",
                    "data":{"user_id":user_id, "name":ret["up_name"], "mobile":ret["up_mobile"], "avatar":img_url}})


class NameHandler(BaseHandler):
    """用户名"""
    @require_logined
    def post(self):
        # 从session中获取用户身份,user_id
        user_id = self.session.data["user_id"]

        # 获取用户想要设置的用户名
        name = self.json_args.get("name")

        # 判断name是否传了，并且不应为空字符串
        # if name == None or "" == name:
        if name in (None, ""):
            return self.write({"errno":RET.PARAMERR, "errmsg":"params error"})

        # 保存用户昵称name，并同时判断name是否重复（利用数据库的唯一索引)
        try:
            self.db.execute_rowcount("update ih_user_profile set up_name=%s where up_user_id=%s", name, user_id)
        except Exception as e:
            logging.error(e)
            return self.write({"errno":RET.DBERR, "errmsg":"name has exist"})

        # 修改session数据中的name字段，并保存到redis中
        self.session.data["name"] = name
        try:
            self.session.save()
        except Exception as e:
            logging.error(e)
        self.write({"errno":RET.OK, "errmsg":"OK"})

class AuthHandler(BaseHandler):
    """实名认证"""
    @require_logined
    def get(self):
        # 在session中获取用户user_id
        user_id = self.session.data["user_id"]

        # 在数据库中查询信息
        try:
            ret = self.db.get("select up_real_name,up_id_card from ih_user_profile where up_user_id=%s", user_id)
        except Exception as e:
            # 数据库查询出错
            logging.error(e)
            return self.write({"errno":RET.DBERR, "errmsg":"get data failed"})
        logging.debug(ret)
        if not ret:
            return self.write({"errno":RET.NODATA, "errmsg":"no data"})
        self.write({"errno":RET.OK, "errmsg":"OK", "data":{"real_name":ret.get("up_real_name", ""), "id_card":ret.get("up_id_card", "")}})

    @require_logined
    def post(self):
        user_id = self.session.data["user_id"]
        real_name = self.json_args.get("real_name")
        id_card = self.json_args.get("id_card")
        if real_name in (None, "") or id_card in (None, ""):
            return self.write({"errno":RET.PARAMERR, "errmsg":"params error"})
        # 判断身份证号格式
        try:
            self.db.execute_rowcount("update ih_user_profile set up_real_name=%s,up_id_card=%s where up_user_id=%s", real_name, id_card, user_id)
        except Exception as e:
            logging.error(e)
            return self.write({"errno":RET.DBERR, "errmsg":"update failed"})
        self.write({"errno":RET.OK, "errmsg":"OK"})








