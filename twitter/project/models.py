from django.db import models

class Tweets(models.Model):
    tweet_id = models.CharField(max_length=50, primary_key = True, unique = True)
    user_name = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    user_image = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
