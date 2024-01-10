# SmartyPlans server

## Project setup
### Setup virtual env and pip.
```
$ virtualenv env
```
### Activate virtual env
Linux
```
$ source env/bin/activate
```
Windows
```
> env\bin\activate
```
### Download packages
```
$ pip install -r requirements.txt
```
### .env
Create .env file or rename .env.local to .env

### Do migration
```
$ python manage.py migrate
```
### Run server
```
$ python manage.py runserver
```
