# Generated by Django 2.2 on 2020-11-05 02:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_courselesson_lesson'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courselesson',
            name='lesson',
        ),
    ]
