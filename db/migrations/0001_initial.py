# Generated by Django 3.0.3 on 2021-05-10 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.FileField(blank=True, null=True, upload_to='backend.File/bytes/filename/mimetype')),
            ],
        ),
    ]