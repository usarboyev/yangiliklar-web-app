# Generated by Django 4.1.6 on 2023-02-28 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]