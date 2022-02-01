from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from posts import views

urlpatterns = format_suffix_patterns([
    path('', views.PostViewSet.as_view({'post': 'create'}), name='posts'),
    path('<int:pk>/', views.PostViewSet.as_view({'delete': 'destroy', 'put': 'update', 'patch': 'update', 'get': 'list'}), name='posts'),
    path('<int:post_id>/likes/', views.LikeViewSet.as_view({'post': 'create', 'get': 'list'}), name='likes'),
    path('<int:post_id>/comments/', views.CommentViewSet.as_view({'post': 'create', 'get': 'list'}), name='comments'),
])

