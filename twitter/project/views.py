from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.db.models import Count, Max
import tweepy
from datetime import date, timedelta
import re
from .models import Tweets

consumer_key = ''
consumer_secret = ''

def extract_domain(url):
    count = 0
    for i in range(0, len(url)):
        if url[i] == "/":
            count += 1
        if count == 3:
            break

    return url[0:i]

def home(request):
    key = request.session.get('access_token')
    secret = request.session.get('access_token_secret')
    if key:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(key, secret)
        api = tweepy.API(auth)
        start_date = date.today()
        end_date = start_date# - timedelta(days=7)

        """
        for tweet in tweepy.Cursor(api.home_timeline, since=end_date).items(100):
            url = tweet.entities['urls']
            if url:
                expanded_url = url[0]['expanded_url']
                domain = extract_domain(expanded_url)
                id = tweet.id
                user_name = tweet.user.name
                text = tweet.text
                image = tweet.user.profile_image_url

                t = Tweets(tweet_id=id, user_name=user_name, text=text, user_image= image, domain=domain)
                t.save()
            """

        tweets = Tweets.objects.all()
        return render(request, 'view_tweets.html', {'screen_name': api.me().screen_name, 'posts': tweets})

    return render(request, 'layout.html')

def login(request):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')
    request.session['request_token'] = auth.request_token
    return redirect(redirect_url)

def callback(request):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    request_token = request.session.get('request_token')
    request.session.delete('request_token')
    verifier = request.GET.get('oauth_verifier')
    auth.request_token = request_token

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error, failed to get access token')

    request.session['access_token'] = auth.access_token
    request.session['access_token_secret'] = auth.access_token_secret

    login(request)

    return redirect('home')

def logout(request):
    request.session.clear()
    #logout(request)
    return redirect('home')

def top_user(request):
    users = Tweets.objects.values('user_name', 'user_image').order_by().annotate(Count("user_name"))
    count = 0
    for x in users:
        if x['user_name__count'] > count:
            user = x['user_name']
            image = x['user_image']
            count = x['user_name__count']

    return render(request, 'top_user.html', {'user':user, 'count':count, 'image':image})

def top_domain(request):
    return render(request, 'top_domain.html')
