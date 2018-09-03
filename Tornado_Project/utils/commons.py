# !/usr/bin/python
# -*- encoding: utf-8 -*-
# @author:spider1998
from utils.response_code import RET
import functools
def require_logined(fun):
    @functools.wraps(fun)
    def wrapper(request_handler_obj,*args,**kwargs):
        if not request_handler_obj.get_current_user():
            request_handler_obj.write(dict(errno=RET.SESSIONERR, errmsg="用户未登录"))
        else:
            fun(request_handler_obj, *args, **kwargs)

    return wrapper