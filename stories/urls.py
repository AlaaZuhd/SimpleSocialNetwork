from django.urls import path, include
from stories import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns([
    path('', views.StoryViewSet.as_view({'post': 'create', 'get': 'list'}), name='stories'),
])

