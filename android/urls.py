from django.urls import path
from rest_framework.routers import SimpleRouter
from .api_views import AppViewSet
from user.views import home

approuter = SimpleRouter()
approuter.register(r'apps_view', AppViewSet, basename='apps_view')

urlpatterns = [
    path('', home, name='home'),
]

urlpatterns += approuter.urls
