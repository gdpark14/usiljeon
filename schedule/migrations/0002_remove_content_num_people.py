# Generated by Django 3.1.1 on 2020-09-17 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='num_people',
        ),
    ]
