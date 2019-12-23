# Generated by Django 2.0.7 on 2018-11-11 18:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hots_title', models.CharField(max_length=500)),
                ('hots_image', models.FileField(upload_to='')),
                ('description', models.TextField(help_text='Enter you blog text here.', max_length=20000)),
                ('post_date', models.DateField(default=datetime.date.today)),
            ],
        ),
    ]
