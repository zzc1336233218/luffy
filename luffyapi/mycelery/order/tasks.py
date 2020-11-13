from celery_tasks.main import app
from orders.models import Order
from datetime import datetime
from django.conf import settings
@app.task(name="check_order")
def check_order():
    # 查询出所有已经超时的订单
    # 超时条件： 当前时间 > (订单生成时间 + 超时时间)   =====>>>>  (当前时间 - 超时时间) > 订单生成时间
    now = datetime.now().timestamp()
    timeout_number = now - settings.ORDER_TIMEOUT
    timeout = datetime.fromtimestamp(timeout_number)
    timeout_order_list = Order.objects.filter(order_status=0, created_time__lte=timeout)
    for order in timeout_order_list:
        order.order_status = 3
        order.save()