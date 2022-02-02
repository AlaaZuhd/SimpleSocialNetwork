from django.urls import path
from profile_app import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = format_suffix_patterns([
    path('', views.ProfileViewSet.as_view({'get': 'list', 'get': 'retrieve', 'post': 'create', 'put': 'update'}), name='profiles'),
    path('<int:pk>/', views.ProfileViewSet.as_view({'get': 'retrieve'}),
         name='profiles'),
    path('<str:pk>/', views.ProfileViewSet.as_view({'put': 'update'}),
         name='profiles'),

])

