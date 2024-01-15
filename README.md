# SmartyPlants Server

## Project setup
### Setup virtual env and pip.
Windows
```
> python -m venv env
```
Linux
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
Create .env file or rename .env.local to .env and set your ip address in ALLOWED_HOSTS


### Change directory
```
cd plantserver
```
### Do migration
```
$ python manage.py migrate
```
### Create superuser
```
$ python manage.py createsuperuser
```
### Opctional: Generate fake data
```
$ python data_generator.py
```
### Run server
```
$ python manage.py runserver 0.0.0.0:8000
```
