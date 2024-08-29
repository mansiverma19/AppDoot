from rest_framework import viewsets, status
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import App, UserApps
from .serializers import AppSerializer, UserAppsSerializer
from user.serializers import *
from django.conf import settings

class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [IsAuthenticated]

    # Upload a new app
    @action(detail=False, methods=['post'])
    def upload_app(self, request):
        serializer = AppSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'App uploaded successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # Handle user tasks (completed, pending, uncompleted apps)
    @action(detail=False, methods=['get'])
    def user_tasks(self, request):
        user = request.user
        completed_tasks = UserApps.objects.filter(user=user, is_completed=True)
        pending_tasks = UserApps.objects.filter(user=user, is_completed=False)
        uncompleted_apps = App.objects.exclude(userapps__user=user)

        data = {
            'MEDIA_URL': settings.MEDIA_URL,
            'completed_tasks': UserAppsSerializer(completed_tasks, many=True).data,
            'pending_tasks': UserAppsSerializer(pending_tasks, many=True).data,
            'uncompleted_apps': AppSerializer(uncompleted_apps, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)

