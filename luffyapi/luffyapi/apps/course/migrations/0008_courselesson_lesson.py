# Generated by Django 2.2 on 2020-11-05 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_auto_20201105_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='courselesson',
            name='lesson',
            field=models.IntegerField(default=1, verbose_name='第几课时'),
            preserve_default=False,
        ),
    ]