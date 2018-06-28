This project search user's from github on basis of there name, number of repos and number of followers.
The search api returns 30 results max per page.

STACK USED -   
    Python (3.6.3)
    Django (2.0)
    DJANGO REST FRAMEWORK
    DATABASE - POSTGRESQL


DATABASE SETTINGS USED - 

    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', -> Engine(psycopg2-binary needed)
        'NAME': 'git_userdb', -> (db name)
        'USER' : 'database_user', -> (db user)
        'PASSWORD' : 'password123', -> (db password (can be anything))
        'HOST' : 'localhost', 
        'PORT' : 5432
    }
    }

-> PLEASE USE THIS COMMAND TO CREATE TABBLES IN POSTGRES DATABASE IN FOLLOWING ORDER: - 
    
    python manage.py makemigrations accounts
    python manage.py migrate
    RUN THIS INSIDE A VIRTUAL ENVIROMENT

Reason to use postgresql database was to hold a lot of user data that was returned from github search api and if needed tha data can be served more faster.


USEFUL API ENDPOINT - 

1-> To search user on the basis of their name and number of repos and number of followers.

    URL - localhost:8000/api/account/?user_name=nikhil&followers=0&repos=0&page=1

    PARAMETERS - 

    user_name -> required (the result will be fetched on the basis of this parameter)

    All other parameters are optional and page parameter will give another set of results if available.

2 -> REPROT PAGE

    Please use this link -> localhost:8000/admin/report to see the stats of how many user a day week and month and also for the api hit's

3 -> A search filter is also applied to search the user on basis of date added and user's login username.

4-> Thumbnail of the user avatar is also availble for every user if avatar_url is not "".