from django.urls import path, include
from rest_framework import routers

from account import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token


# account_router = routers.DefaultRouter()
# account_router.register('accounts', views.AccountViewSet, basename='accounts')

urlpatterns = format_suffix_patterns([
    path('/', views.AccountViewSet.as_view({'delete': 'destroy', 'post': 'create'}), name='accounts-delete'),
    path('/change-password/', views.AccountViewSet.as_view({'put': 'update'}), name='change-password'),
])


