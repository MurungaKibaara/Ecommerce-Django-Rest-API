[![Build Status](https://api.travis-ci.com/MurungaKibaara/eretail.svg?token=zZRZqvQuzNU61ipLVxk4&branch=develop)](https://travis-ci.com/MurungaKibaara/eretail)
[![codecov](https://codecov.io/gh/MurungaKibaara/eretail/branch/develop/graph/badge.svg?token=5G2Q7OAFSU)](https://codecov.io/gh/MurungaKibaara/eretail?token=5G2Q7OAFSU)



# E-RETAIL API - Version 1

A multi-level e-commerce API created using the Django REST Framework.

## Features

## Documentation

## Getting Started

### Installation and setup
Clone this repository
> git clone https://github.com/MurungaKibaara/eretail.git

### Navigate to the project directory

> cd _path to project directory_

### Install Python

> https://www.python.org/downloads/release/python-362/

### Install virtualenv

> pip install virtualenv

### Install virtualenvwrapper-win

> pip install virtualenvwrapper

### Make a virtual environment

> mkvirtualenv _project-name_

### Activate your environment

> source _folder_to_env/bin/activate

### Requirements

All the requirements for the project are located in the requirements.txt file in the project root.  
You can automatically install all of them by typing:  

> pip install -r requirements.txt

### Database

You can use any database you please but by default the app uses PostgreSQL.
Create your database and make migrations:

> python manage.py makemigrations

Then migrate the changes:

> python manage.py migrate

### Testing the application
> python manage.py test

### Running the application
First you must export or set the environment variables like so:
> export DATABASE_NAME=db_name
export DATABASE_USER=postgres_user
export DATABASE_PASSWORD=db_password

Then run the application using:
> python manage.py runserver
