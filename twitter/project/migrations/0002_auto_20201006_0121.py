# Generated by Django 3.1.2 on 2020-10-05 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweets',
            name='tweet_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
    ]
