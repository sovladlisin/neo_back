# Generated by Django 3.0.3 on 2021-12-12 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_editor',
            field=models.BooleanField(default=False),
        ),
    ]
