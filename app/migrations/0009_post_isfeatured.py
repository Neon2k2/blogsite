# Generated by Django 4.2 on 2023-04-22 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_subscribe'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='isfeatured',
            field=models.BooleanField(default=False),
        ),
    ]