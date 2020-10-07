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
    """
        The first page on the website which shows all the tweets
        and provides option for sign in with twitter
    """
    tweets = Tweets.objects.all() #extracts all the tweets from the database
    tweets = tweets[::-1]
    name = request.session.get('screen_name')
    return render(request, 'view_tweets.html', {'screen_name': name, 'posts': tweets})


def extract_domain(url):
    """
        This function is passed the expanded url and returns only the domain name of the website
        It is only used by persist_tweets()
    """
    count = 0
    start = 0
    for i in range(0, len(url)):
        if url[i] == "/":
            count += 1
            if count == 2:
                start = i+1
            elif count == 3:
                break

    return url[start:i]


def persist_tweets(request):
    """
        This is only called once when the user tries to sign in 
        and when called upon it creates an api instance and extracts 
        tweets for the past 7 days from the user's home timeline and 
        adds the tweet_id, text, domain, user_image_url in the database
    """
    
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
            id = tweet.id  #the id of a tweet
            user_name = tweet.user.name  #the name of the user who tweeted
            text = tweet.text  #the content of the tweet
            image = tweet.user.profile_image_url  #the profile image of the user

            t = Tweets(tweet_id=id, user_name=user_name, text=text, user_image= image, domain=domain)
            t.save() #for adding tweets to the database

    return redirect('home')


def login(request):
    """
        As the user clicks on sign in this function starts working.
        this fetches the twitter authorization url and redirects the to it.
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')
    request.session['request_token'] = auth.request_token
    return redirect(redirect_url)


def callback(request):
    """
        After authentication on twitter, user gets back on this where the user's
        details are extracted and saved in session.
        Then it goes to persist_tweets() to add tweets to database which then takes
        the user to the home page which displays all the tweets.
    """
    
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
    """
        The simple task of logout is performed, which deletes user information from the session.
    """
    request.session.clear()
    return redirect('home')


def top_user(request):
    """
        Computes and displays the user who shared the most links.
    """
    name = request.session.get('screen_name')
    if not name:
        return redirect('login')
    users = Tweets.objects.values('user_name', 'user_image').order_by().annotate(Count("user_name"))
    user = max(users, key=lambda kv:kv['user_name__count'])
    return render(request, 'top_user.html', {'screen_name': name, 'user':user})


def top_domain(request):
    """
        Computes and displays the list of all domains ranking them in order of count of their occurance.
    """
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
