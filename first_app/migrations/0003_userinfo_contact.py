# Generated by Django 3.0.2 on 2020-05-27 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_auto_20200527_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='contact',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]