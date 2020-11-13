# Generated by Django 2.2 on 2020-11-11 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pay_type',
            field=models.SmallIntegerField(choices=[(0, '支付宝'), (1, '微信支付')], default=1, verbose_name='支付方式'),
        ),
    ]