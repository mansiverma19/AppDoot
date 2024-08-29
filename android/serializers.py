from rest_framework import serializers
from .models import *


class AppSerializer(serializers.ModelSerializer):

     class Meta:
        model = App
        fields = '__all__'

class UserAppsSerializer(serializers.ModelSerializer):

     class Meta:
        model = UserApps
        fields = '__all__'