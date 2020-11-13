from django.shortcuts import render
pc_geetest_id = "5e876edb2bda195c265416b70e7389a7"
pc_geetest_key = "c1f0f6f5958507924d187db31cd136e5"
# Create your views here.
from luffyapi.libs.geetest import GeetestLib
from rest_framework.response import Response
from .utils import get_user_by_account
from rest_framework import status as http_status
from rest_framework.views import APIView
class CaptchaAPIView(APIView):
    """验证码视图类"""
    status = False
    user_id = 0
    def get(self,request):
        """获取验证码"""
        username = request.query_params.get("username")
        user = get_user_by_account(username)
        if user is None:
            return Response({"message":"对不起，用户不存在！"},status=http_status.HTTP_400_BAD_REQUEST)

        self.user_id = user.id
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)
        # todo 后面增加status和user_id保存到redis数据库
        response_str = gt.get_response_str()
        return Response(response_str)

    def post(self,request):
        """验证码的验证方法"""
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        if self.status:
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status":"success"} if result else {"status":"fail"}
        return Response(result)

from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import UserModelSerializer
class UserAPIView(CreateAPIView):
    """用户信息视图"""
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

"""
GET /user/mobile/<mobile>/
"""
import re
from rest_framework import status
class MobileAPIView(APIView):
    def get(self,request,mobile):
        ret = get_user_by_account(mobile)
        if ret is not None:
            return Response({"message":"手机号已经被注册过！"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"ok"})

import random
from django_redis import get_redis_connection
from luffyapi.settings import constants
from luffyapi.libs.yuntongxun.sms import CCP

import logging
log = logging.getLogger("django")

class SMSAPIView(APIView):
    def get(self,request,mobile):
        """短信发送"""

        # 1. 判断手机号码是否在60秒内曾经发送过短信
        redis_conn = get_redis_connection("sms_code")
        ret = redis_conn.get("mobile_%s" % mobile)
        if ret is not None:
            return Response({"message":"对不起，60秒内已经发送过短信，请耐心等待"},status=status.HTTP_400_BAD_REQUEST)

        # 2. 生成短信验证码
        sms_code = "%06d" % random.randint(1, 999999)

        # 3. 保存短信验证码到redis[使用事务把多条命令集中发送给redis]
        # 创建管道对象
        pipe = redis_conn.pipeline()
        # 开启事务【无法管理数据库的读取数据操作】
        pipe.multi()
        # 把事务中要完成的所有操作，写入到管道中
        pipe.setex("sms_%s" % mobile, constants.SMS_EXPIRE_TIME, sms_code)
        pipe.setex("mobile_%s" % mobile, constants.SMS_INTERVAL_TIME,"_")
        # 执行事务
        pipe.execute()

        # 4. 调用短信sdk，发送短信
        try:
            from mycelery.sms.tasks import send_sms
            send_sms.delay(mobile,sms_code)

            # ccp = CCP()
            # ret = ccp.send_template_sms(mobile, [sms_code, constants.SMS_EXPIRE_TIME//60], constants.SMS_TEMPLATE_ID)
            # if not ret:
            #     log.error("用户注册短信发送失败！手机号：%s" % mobile)
            #     return Response({"message":"发送短信失败！"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            return Response({"message":"发送短信失败！"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 5. 响应发送短信的结果
        return Response({"message":"发送短信成功！"})

from rest_framework.generics import ListAPIView
from order.models import Order
from .serializers import UserOrderModelSerializer
from rest_framework.permissions import IsAuthenticated
class UserOrderAPIView(ListAPIView):
    serializer_class = UserOrderModelSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Order.objects.filter(user_id=self.request.user.id)