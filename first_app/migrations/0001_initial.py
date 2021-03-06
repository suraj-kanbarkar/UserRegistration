# Generated by Django 3.0.2 on 2020-05-29 08:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.CharField(auto_created=True, blank=True, max_length=255, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('contact', models.CharField(blank=True, max_length=128, null=True)),
                ('designation', models.CharField(blank=True, max_length=128, null=True)),
                ('salary', models.CharField(blank=True, max_length=15, null=True)),
                ('is_approved', models.NullBooleanField()),
                ('invalid_login_attempts', models.IntegerField(default=0)),
                ('last_invalid_time', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
