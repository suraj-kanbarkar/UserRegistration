# Generated by Django 3.0.2 on 2020-05-27 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0003_userinfo_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='salary',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
