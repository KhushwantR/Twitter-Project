# Twitter Project using Tweepy

Website URL: https://twitter-links.herokuapp.com/

This Django based Web application uses Twitter Api Tweepy for authentication and also provides the following functionalities:
1. Shows all the Tweets of Users home timeline that have URL in them, after the user sign-in.
2. Computes and shows the Top Twitter user who has shared the most links based on the home timeline of the users who signed in on this app.
3. Computes and shows a list of Top Domains which were shared by users based on the home timeline of the users who signed in on this app.

# Tech Stack Used

1. Python 3.8.2
2. Django 3.1.2
3. HTML 5
4. CSS 3
5. PostgresSQL
6. Tweepy API

# Steps to Compile and Run the App

1. Simply Download the ZIP file of the code from github or clone this repository using the Command
```sh
   git clone https://github.com/KhushwantR/Twitter-Project
```

2. Install Pip if not installed already

3. Create a virtual environment and activate it.

4. Create a Twitter Developer and create a project to generate Consumer_key and Consumer_secret and add them in the project/views.py file.

5. Create a Database and replace the credentials in the project/settings.py file in the Database section.

6. Install all the required packages using the command
```sh
   pip install -r requirements.txt
```
7. Migrate the tables to the database you created using the command:
```sh
   python manage.py makemigrations
   python manage.py migrate
```
8. Finally you are ready to run this app locally, use the command:
```sh
   python manage.py runserver
```
9. Copy and paste the url from the terminal to your browser.



