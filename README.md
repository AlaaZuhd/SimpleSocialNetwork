# SimpleSocialNetwork

## Steps needed for running this project: 

### 1- install the needed packages: 
#### pip install -r requirements.txt 
### 2- run the project in the production mode: 
#### python manage.py runserver --settings=simple_social_network.production_settings
### 3- run the celery worker to do the tasks in the background: 
#### celery -A simple_social_network.celery worker --pool=solo -l info
### 4- run the celery worker to do the tasks periodically: 
#### celery -A simple_social_network beat -l info

## Endpoints: 
### 1- for accounts app:
#### localhost:8000/accounts/
#### localhost:8000/accounts/id/

### 2- for profile app: 
#### localhost:8000/profiles/
#### localhost:8000/profiles/id/ --> id: profile id or 'me' as the profile id for the current user

### 3- for posts app: 
#### localhost:8000/posts/
#### localhost:8000/posts/id/
#### localhost:8000/posts/id/comments/ --> comments associated with the /posts/id/
#### localhost:8000/posts/id/comments/id/ --> comment associated with the posts/id/
#### localhost:8000/comments/
#### localhost:8000/comments/id/
#### localhost:8000/posts/id/likes/ --> likes associated with the /posts/id/
#### localhost:8000/posts/id/likes/id/ --> likes associated with the posts/id/
#### localhost:8000/likes/
#### localhost:8000/likes/id/

### 4- for friends app: 
#### localhost:8000/friends/
#### localhost:8000/friends/id/ 
#### localhost:8000/friends/send_friend_request/ --> sending a friend reqeust with specifying the other user in the request body as "to_user_id"
#### localhost:8000/friends/show_mutual_friends/ --> displaying the mutual friends between the two users ("first_user_id" and "second_user_id" from the request body)
#### localhost:8000/friends/unfriend/ --> removing a user from the list of friends by specifying the user id in the url


### 5- for stories app:
#### localhost:8000/stories/
#### localhost:8000/stories/id/ 
#### localhost:8000/friends_stories/ --> listing the stories of the user's friends