# Generated by Django 3.1.2 on 2020-10-05 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweets',
            fields=[
                ('tweet_id', models.IntegerField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('user_name', models.CharField(max_length=255)),
                ('text', models.CharField(max_length=255)),
                ('user_image', models.CharField(max_length=255)),
                ('domain', models.CharField(max_length=255)),
            ],
        ),
    ]
