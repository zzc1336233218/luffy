from luffyapi.settings import constants


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    :param token 本次登录成功以后，返回的jwt
    :param user  本次登录成功以后，从数据库中查询到的用户模型信息
    :param request 本次客户端的请求对象
    """
    return {
        'token': token,
        'id': user.id,
        'username': user.username,
        "user_credit": user.credit,
        "credit_to_money": constants.CREDIT_MONEY,
    }


def get_user_by_account(account):
    """
    根据帐号获取user对象
    :param account: 账号，可以是用户名username，也可以是手机号mobile, 或者其他的数据
    :return: User对象 或者 None
    """
    try:
        user = User.objects.filter( Q(username=account) | Q(mobile=account) ).first()
    except User.DoesNotExist:
        return None
    else:
        return user


from .models import User
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user is not None and user.check_password(password) and user.is_authenticated:
            return user
        else:
            return None
