"""simple_social_network URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings

from friends import views as friend_views
from profile_app import views as profile_views
from posts import views as posts_views
from stories import views as stories_views
from account import views

account_router = routers.DefaultRouter()
account_router.register('', views.AccountViewSet, basename='accounts')

friend_requests_router = routers.DefaultRouter()
friend_requests_router.register('', friend_views.FriendViewSet, basename='friends')

profile_app_router = routers.DefaultRouter()
profile_app_router.register('', profile_views.ProfileViewSet, basename='profiles')

posts_router = routers.DefaultRouter()
posts_router.register('', posts_views.PostViewSet, basename='posts')

likes_router = routers.DefaultRouter()
likes_router.register('', posts_views.LikeViewSet, basename='likes')

comments_router = routers.DefaultRouter()
comments_router.register('', posts_views.CommentViewSet, basename='comments')

stories_router = routers.DefaultRouter()
stories_router.register('', stories_views.StoryViewSet, basename='stories')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include(account_router.urls)),
    path('accounts/', include('account.urls')),

    path('profiles/', include(profile_app_router.urls)),
    path('profiles/', include('profile_app.urls')),

    path('posts/', include(posts_router.urls)),
    path('posts/<int:post_id>/likes/', include(likes_router.urls)),
    path('likes/', include(likes_router.urls)),
    path('posts/<int:post_id>/comments/', include(comments_router.urls)),
    path('comments/', include(comments_router.urls)),

    path('friends/', include(friend_requests_router.urls)),

    path('stories/', include(stories_router.urls)),
]

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # utilizing the medial directory.
