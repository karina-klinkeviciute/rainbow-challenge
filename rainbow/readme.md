# Rainbow challenge

## Launching Django project

1. create some directory and clone the repository 

2. create virtual environment next to the repository:

`python3 -m venv venv`

3. activate the virtual environment:

Linux/MacOS:
`source venv/bin/activate`

Windows:
`venv\Scripts\activate`

4. cd into the project:
`cd rainbow/rainbow/`
   
5. create database

create empty database in the mysql 

5. clone the environment file

in this directory there's a file `.env_example` - you should copy it to a file called `.env` and change those settings there to your own:

```
DJANGO_PROJECT_PATH=/home/karina/work/rainbow/rainbow
DJANGO_SECRET_KEY=add_one

DB_USER=rainbow
DB_HOST=localhost
DB_PASSWORD=add_one
```

6. run django server:
python manage.py runserver
   
This will start Django server on port 8000

You will be able to access it here: http://127.0.0.1:8000/ 

