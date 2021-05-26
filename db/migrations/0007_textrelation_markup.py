# Generated by Django 3.0.3 on 2021-05-23 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0006_markup_ontology_uri'),
    ]

    operations = [
        migrations.AddField(
            model_name='textrelation',
            name='markup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relation_markup', to='db.Markup'),
        ),
    ]
