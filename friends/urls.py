from django.urls import path, include
from rest_framework import routers

from friends import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns([
    path('send-friend-request/<int:to_user_id>/', views.send_friend_request, name='send-friend-request'),
    path('accept-friend-request/<int:friend_request_id>/', views.accept_friend_request, name='accept-friend-request'),
    path('me/', views.show_my_friends, name='show-my-friends'),
    path('<int:pk>/', views.unfriend, name='unfriend'),
    path('mutual/<int:first_user_id>/<int:second_user_id>/', views.show_mutual_friends, name='mutual-friends')

])

