from celery import Celery

# 创建celery主程序对象
app = Celery("luffy")

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luffyapi.settings.dev')
import django
django.setup()

# 加载配置
app.config_from_object("mycelery.config")

# 注册任务
app.autodiscover_tasks(["mycelery.sms","mycelery.mail","mycelery.order"])

# 通过终端来启动celery
# celery -A mycelery.main worker --loglevel=info