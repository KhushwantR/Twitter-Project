from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
import tweepy

consumer_key = ''
consumer_secret = ''

def home(request):
    key = request.session.get('access_token')
    secret = request.session.get('access_token_secret')
    if key:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(key, secret)
        api = tweepy.API(auth)
        return render(request, 'layout.html', {'screen_name': api.me().screen_name})

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

    auth.set_access_token(auth.access_token, auth.access_token_secret)
    api = tweepy.API(auth)
    login(request)

    return redirect('home')

def logout(request):
    request.session.clear()
    #logout(request)

    return redirect('home')
