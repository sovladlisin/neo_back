# Generated by Django 3.0.3 on 2021-05-10 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_auto_20210510_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='name',
            field=models.CharField(default='Не указано', max_length=500),
        ),
    ]
