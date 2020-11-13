from rest_framework import serializers
from .models import Order,OrderDetail
from django_redis import get_redis_connection
from datetime import datetime
from course.models import Course,CourseExpire
from django.db import transaction
from coupon.models import UserCoupon
from luffyapi.settings import constants

class OrderModelSerializer(serializers.ModelSerializer):
    """订单序列化器"""

    class Meta:
        model = Order
        fields = ["id", "order_number", "pay_type", "credit", "coupon"]
        extra_kwargs = {
            "id":{"read_only": True},
            "order_number": {"read_only": True},
            "pay_type": {"write_only": True},
            "credit": {"write_only": True},
            "coupon": {"write_only": True}
        }

    def validate(self, attrs):
        # 验证数据
        pay_type = attrs.get("pay_type")
        try:
            Order.pay_choices[pay_type]
        except:
            raise serializers.ValidationError("对不起，当前不支持选中的支付方式！")

        # todo 判断积分使用是否上限
        user_credit = self.context["request"].user.credit
        credit = attrs.get("credit",0)
        if credit != 0  and user_credit < credit:
            raise serializers.ValidationError("对不起，当前使用积分超过上限！")

        # todo 判断优惠券是否在使用期间，是否是未使用状态
        user_coupon_id = attrs.get("coupon")
        if user_coupon_id > 0:
            now = datetime.now()
            now_time = now.strftime("%Y-%m-%d %H:%M:%S")
            try:
                user_coupon = UserCoupon.objects.get(pk=user_coupon_id,start_time__lte=now_time,is_show=True,is_deleted=False, is_use=False)
            except:
                raise serializers.ValidationError("对不起，当前优惠券不可用或者不存在！")

            timer_timestamp = user_coupon.coupon.timer * 24 * 60 *60
            start_timestamp = user_coupon.start_time.timestamp()
            end_timestamp = start_timestamp + timer_timestamp
            if end_timestamp < now.timestamp():
                raise serializers.ValidationError("对不起，当前优惠券不可用或者不存在！")

        # 一定要 return 验证结果
        return attrs

    def create(self, validated_data):
        """生成订单[使用事务来完成订单的生成]"""
        # 生成唯一订单号[结合时间+用户ID+随机数(递增值<在redis中针对一个数值不断递增>)]
        redis_conn = get_redis_connection("cart")
        # 调用序列化器 OrderSerializer(instance="模型对象",data=data,context={"views":"视图对象","request":"请求对象"....})
        user_id = self.context["request"].user.id
        incr = int( redis_conn.incr("order") )
        order_number = datetime.now().strftime("%Y%m%d%H%M%S") + "%06d" % user_id + "%06d" % incr

        with transaction.atomic():
            # 记录事务回滚点
            save_id = transaction.savepoint()
            # 生成订单
            order = Order.objects.create(
                order_title="路飞学城课程购买",
                total_price=0,
                real_price=0,
                order_number=order_number, # 订单号
                order_status=0,
                pay_type=validated_data.get("pay_type"),
                credit=validated_data.get("pay_type",0),
                coupon=validated_data.get("pay_type",0),
                order_desc="",
                user_id=user_id
            )

            # 然后生成订单详情[记录本次下单的所有商品课程信息]
            cart_bytes_dict = redis_conn.hgetall("cart_%s" % user_id )
            selected_bytes_list = redis_conn.smembers("selected_%s" % user_id )

            # 开启redis事务操作
            pipe = redis_conn.pipeline()
            pipe.multi()

            # 获取勾选的商品
            for course_id_bytes,expire_id_bytes in cart_bytes_dict.items():
                course_id = int( course_id_bytes.decode() )
                expire_id = int( expire_id_bytes.decode() )
                # 判断商品课程ID是否在勾选集合中
                if course_id_bytes in selected_bytes_list:
                    try:
                        course = Course.objects.get(is_show=True, is_deleted=False, pk=course_id)
                    except Course.DoesNotExist:
                        # 回滚事务[把save_id声明到这里的中间所有执行的sql语句执行产生的影响抹除]
                        transaction.savepoint_rollback(save_id)
                        raise serializers.ValidationError("对不起，购买的商品不存在或者已下架！")

                    # 判断课程有效期，获取课程原价
                    original_price = course.price
                    try:
                        if expire_id > 0:
                            coruseexpire = CourseExpire.objects.get(id=expire_id)
                            original_price = coruseexpire.price
                    except CourseExpire.DoesNotExist:
                        pass

                    real_price = course.real_price(expire_id)
                    # 生成订单详情
                    try:
                        OrderDetail.objects.create(
                            order=order,
                            course=course,
                            expire=expire_id,
                            price=original_price,
                            real_price=real_price,
                            discount_name=course.discount_name
                        )
                    except:
                        transaction.savepoint_rollback(save_id)
                        raise serializers.ValidationError("对不起，订单生成失败！")

                    # 计算订单总价
                    order.total_price += float(real_price)

                    # 移除掉已经加入到订单里面的购物车商品
                    pipe.hdel("cart_%s" % user_id, course_id)
                    pipe.srem("selected_%s" % user_id, course_id)

            # 默认最终实付价格是订单总价
            real_price = order.total_price

            try:
                # 对总价格加入优惠券折扣
                user_coupon_id = validated_data.get("coupon")
                if user_coupon_id > 0:
                    user_coupon = UserCoupon.objects.get(pk=user_coupon_id)
                    if user_coupon.coupon.condition > order.total_price:
                        """如果订单总金额比使用条件价格低，则报错！"""
                        transaction.savepoint_rollback(save_id)
                        raise serializers.ValidationError("对不起，订单生成失败！当前购物车中购买商品总价格没达到使用该优惠券的价格条件")

                    sale_num = float( user_coupon.coupon.sale[1:] )
                    if user_coupon.coupon.sale[0] == "*":
                        """折扣优惠"""
                        real_price = order.total_price * sale_num
                    else:
                        """减免优惠"""
                        real_price = order.total_price - sale_num

                    order.coupon = user_coupon_id

                # 对总价格加入积分抵扣
                credit = validated_data.get("credit")
                if credit > 0:
                    # 判断积分是否超过订单总价格的折扣比例
                    if credit > real_price * constants.CREDIT_MONEY:
                        transaction.savepoint_rollback(save_id)
                        raise serializers.ValidationError("对不起，订单生成失败！当前订单中使用的积分超过使用上限！")

                    real_price = float("%.2f" % (real_price - credit / constants.CREDIT_MONEY))
                    order.credit = credit

                order.real_price = real_price
                order.save()
                pipe.execute()
            except:
                transaction.savepoint_rollback(save_id)
                raise serializers.ValidationError("对不起，订单生成失败！")

        # 返回生成的模型
        return order