# Generated by Django 4.1.1 on 2022-11-06 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='position',
        ),
    ]
