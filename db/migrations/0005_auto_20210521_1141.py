# Generated by Django 3.0.3 on 2021-05-21 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0004_auto_20210520_1556'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resource',
            old_name='original_text_uri',
            new_name='original_object_uri',
        ),
    ]
