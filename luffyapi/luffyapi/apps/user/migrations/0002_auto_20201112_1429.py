# Generated by Django 2.2 on 2020-11-12 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='credit',
            field=models.IntegerField(blank=True, default=0, verbose_name='贝壳'),
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_show', models.BooleanField(default=False, verbose_name='是否显示')),
                ('orders', models.IntegerField(default=1, verbose_name='排序')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('opera', models.SmallIntegerField(choices=[(1, '赚取'), (2, '消费')], verbose_name='操作类型')),
                ('number', models.SmallIntegerField(default=0, verbose_name='积分数值')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_credit', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '积分流水',
                'verbose_name_plural': '积分流水',
                'db_table': 'ly_credit',
            },
        ),
    ]
