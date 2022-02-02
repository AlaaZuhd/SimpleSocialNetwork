# SimpleSocialNetwork

## Steps needed for running this project: 

### 1- install the needed packages: 
#### pip install -r requirements.txt 
### 2- run the project: 
#### python manage.py runserver
### 3- run the celery worker to do the tasks in the background: 
#### celery -A simple_social_network.celery worker --pool=solo -l info
### 4- run the celery worker to do the tasks periodically: 
#### celery -A simple_social_network beat -l info

## Endpoints: 
### 1- for accounts app:
#### localhost:8000/accounts