# Generated by Django 4.0.4 on 2022-05-21 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommenderapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='movie_keywords',
            field=models.CharField(default='', max_length=300),
        ),
    ]
