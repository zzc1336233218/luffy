# Generated by Django 2.2 on 2020-11-05 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_remove_courselesson_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='courselesson',
            name='lesson',
            field=models.IntegerField(default=1, verbose_name='第几课时'),
            preserve_default=False,
        ),
    ]
