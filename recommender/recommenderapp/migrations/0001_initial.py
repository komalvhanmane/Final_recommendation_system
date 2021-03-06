# Generated by Django 4.0.4 on 2022-05-27 13:32

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
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.CharField(default='', max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('movie_tags', models.CharField(default='', max_length=300)),
                ('popularity', models.CharField(default='', max_length=300)),
                ('genres', models.CharField(max_length=100)),
                ('cast', models.CharField(default='', max_length=100)),
                ('image', models.ImageField(default='', upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tp', models.DateTimeField(null=True)),
                ('name', models.CharField(max_length=200)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
