# Generated by Django 4.1.3 on 2022-11-07 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_article_body_alter_article_categorie1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='bg',
            field=models.ImageField(blank=True, null=True, upload_to='articles_images'),
        ),
    ]
