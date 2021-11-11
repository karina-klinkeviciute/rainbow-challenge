# Rainbow challenge

## License

Rainbow Challenge is licensed by the MIT license. Full license in the LICENSE file

## About Rainbow Challenge

### Rainbow Challenge project

Rainbow challenge is a project meant to help young LGBTQIA+ activists to get involved in the activism and protection of LGBTQIA rights.

### Rainbow Challenge app

This app helps people, especially youth to get involved in the LGBTQIA+ activism and support in a captivating and rewarding way.

#### How Rainbow Challenge app works

Rainbow challenge app presents a set of challenges of different types. Those include writing of an article, participating in an event or organizing one, telling a story or some other way of contribution to awarance and acceptance of LGBTQIA++ people.

Users can join those challenges and complete them. Each challenge is assigned a value of points, called Rainbows in the app. Users are accumulating those Rainbows.

When a user collects some amount of Rainbows, they can exchange them for selected prizes. Those can be tickets to events, cups, books, tote bags etc.

There will also be streaks - a number of weeks in which user has completed at least one task. If they miss one week, the number is reduced by 1 (instead of getting to 0).

Every user will belong to a certain region and the regions will compete between themselves by the total of Streaks on that week.


## Structure of the Django project

Django project has a few main apps: challenge, joined_challenge, quiz, results, user, news.

`challenge` app has models for each type of challenge, and a generic model for each challenge.

`joined_challenge` app is for data that is saved when users join and complete challenges. It has an identical challenge type structure to the challenge app.

`results` app holds data about the results of completing challenges - regions (for competing), prizes, streaks.

`News` app is ofr the news that are displayed when the user launches an app.

Users won't be able to communicate with each other.

Users should have an option to contact support through the app. This will be done through the messaging system that will also be responsible for sending automated messages about confirming challenges etc.

`quiz` app is for quizzes that are connected to the challenges of quiz type.

## Contributing

Contributors are welcome. If you'd like to contribute, you can write to the email karina.klinkeviciute@gmail.com 

## Launching Django project

1. create some directory and clone the repository 

1. create virtual environment next to the repository:

    Linux/MacOS"
    `python3 -m venv venv`
   
    Windows:
    `py -m venv venv`

1. activate the virtual environment:

    Linux/MacOS:
    `source venv/bin/activate`

    Windows:
    `venv\Scripts\activate`

1. cd into the project:
    `cd rainbow_challenge/rainbow/`
   
1. install requirements

    `pip install -r requirements.txt`

1. create database

    create empty database in the mysql 

1. clone the environment file

    in this directory there's a file `.env_example` - you should copy it to a file called `.env` and change those settings there to your own:

    ```
    DJANGO_PROJECT_PATH=/home/karina/work/rainbow/rainbow
    DJANGO_SECRET_KEY=add_one
    
    DB_USER=rainbow
    DB_HOST=localhost
    DB_PASSWORD=add_one
    ```

1. migrate database:
    `python manage.py migrate`
   
1. create a user (superuser) for yourself:
    `python manage.py createsuperuser`
   and enter the details it asks

1. run django server:
    `python manage.py runserver`
   
    This will start Django server on port 8000
    
    You will be able to access it here: http://127.0.0.1:8000/ 

