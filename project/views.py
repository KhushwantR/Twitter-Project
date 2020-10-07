from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.db.models import Count, Max
from datetime import date, timedelta
from .models import Tweets
import tweepy
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

consumer_key = env('CONSUMER_KEY')
consumer_secret = env('CONSUMER_SECRET')

def home(request):
    tweets = Tweets.objects.all()
    name = request.session.get('screen_name')
    return render(request, 'view_tweets.html', {'screen_name': name, 'posts': tweets})


def extract_domain(url):
    count = 0
    for i in range(0, len(url)):
        if url[i] == "/":
            count += 1
        if count == 2:
            start = i+1
        if count == 3:
            break

    return url[start:i]


def persist_tweets(request):
    key = request.session.get('access_token')
    secret = request.session.get('access_token_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    api = tweepy.API(auth)
    request.session['screen_name'] = api.me().screen_name

    start_date = date.today()
    end_date = start_date - timedelta(days=7)

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
            
    return redirect('home')


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

    persist_tweets(request)
    return redirect('home')



def logout(request):
    request.session.clear()
    return redirect('home')


def top_user(request):
    name = request.session.get('screen_name')
    if not name:
        return redirect('login')
    users = Tweets.objects.values('user_name', 'user_image').order_by().annotate(Count("user_name"))
    user = max(users, key=lambda kv:kv['user_name__count'])
    return render(request, 'top_user.html', {'screen_name': name, 'user':user})


def top_domain(request):
    name = request.session.get('screen_name')
    if not name:
        return redirect('login')
    domains = Tweets.objects.values('domain').order_by().annotate(Count('domain'))
    top_domains = sorted(domains, key=lambda kv:kv['domain__count'], reverse=True)
    i=1
    for x in top_domains:
        x['rank'] = i
        i+=1
    return render(request, 'top_domain.html', {'screen_name': name, 'domains':top_domains})
