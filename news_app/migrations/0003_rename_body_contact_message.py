# Generated by Django 4.1.6 on 2023-02-12 01:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0002_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='body',
            new_name='message',
        ),
    ]
