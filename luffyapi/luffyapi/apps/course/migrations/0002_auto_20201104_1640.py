# Generated by Django 2.2 on 2020-11-04 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_type',
            field=models.SmallIntegerField(choices=[(0, '付费课程'), (1, 'VIP专享'), (2, '学位课程')], default=0, verbose_name='付费类型'),
        ),
        migrations.AlterField(
            model_name='courselesson',
            name='orders',
            field=models.IntegerField(default=1, verbose_name='排序'),
        ),
    ]