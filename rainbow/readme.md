# Rainbow challenge

## License

Rainbow Challenge is licensed by the MIT license. Full license in the LICENSE file.

## About Rainbow Challenge

### Rainbow Challenge project

Rainbow challenge is a project by [Tolerantiško Jaunimo Asociacija](https://tja.lt/) (Tolerant Youth Association). It was designed to help young LGBTQIA+ activists to get involved in the activism and protection of LGBTQIA+ rights.

Website for project: [https://rainbowchallenge.lt/](https://rainbowchallenge.lt/)

Android app can be installed from here: [https://play.google.com/store/apps/details?id=rainbowchallenge.lt.rainbow_challenge](https://play.google.com/store/apps/details?id=rainbowchallenge.lt.rainbow_challenge)

Apple app can be installed from here: [https://apps.apple.com/lt/app/rainbow-challenge-app/id6444240926](https://apps.apple.com/lt/app/rainbow-challenge-app/id6444240926)


### Rainbow Challenge app

This app helps people, especially youth to get involved in the LGBTQIA+ activism in a captivating and rewarding way.

#### Rainbow challenge app code

The backend of the code is written in Python and Django and is in this repository. The frontend is written in Dart and Flutter and is in a repository here: [https://github.com/karina-klinkeviciute/rainbow-challenge-front](https://github.com/karina-klinkeviciute/rainbow-challenge-front) 

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

[More about the app structure](docs/app_structure.md)

## Contributing

Contributors are welcome. If you'd like to contribute, you can write to the email karina.klinkeviciute@gmail.com 

## Launching Django project

1. create some directory and clone the repository 

2. create virtual environment next to the repository:

    Linux/MacOS"
    `python3 -m venv venv`
   
    Windows:
    `py -m venv venv`

3. activate the virtual environment:

    Linux/MacOS:
    `source venv/bin/activate`

    Windows:
    `venv\Scripts\activate`

4. cd into the project:
    `cd rainbow_challenge/rainbow/`
   
5. install requirements

    `pip install -r requirements.txt`

6. create database

    create an empty `postgresql` database called `rainbow`. Must be accessible at port `5432`

7. clone the environment file

    in this directory there's a file `.env_example` - you should copy it to a file called `.env` and change those settings there to your own:

    ```
    DJANGO_PROJECT_PATH=/home/karina/work/rainbow/rainbow
    DJANGO_SECRET_KEY=add_one
    
    DB_USER=rainbow
    DB_HOST=localhost
    DB_PASSWORD=add_one
    ```

8. migrate database:
    `python manage.py migrate`
   
9. create a user (superuser) for yourself:
    `python manage.py createsuperuser`
   and enter the details it asks

10. run django server:
     `python manage.py runserver`
   
     This will start Django server on port 8000
    
     You will be able to access it here: http://127.0.0.1:8000/ 

11. run celery: 
    `celery -A rainbow_project worker -B --detach -f celery.log --loglevel=DEBUG`
    Checking for celery status: `celery -A rainbow_project status`

12. run tests:
    ```bash
    $ pytest
    ```

## Further documentation

Further documentation is [here](docs/index.md)
