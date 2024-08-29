from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from .models import Profile, User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, ProfileSerializer

class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    # Register a new user
    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            profile = Profile.objects.create(user=user)  # Automatically create a profile
            return Response({'status': 'user created', 'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login', url_name='login')
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                django_login(request, user)  # Log in the user
                refresh = RefreshToken.for_user(user)
                return Response({
                    'status': 'login successful',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_data': UserSerializer(user).data,
                    'profile': ProfileSerializer(user.profile).data if hasattr(user, 'profile') else None
                }, status=status.HTTP_200_OK)
            return Response({'error': 'invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='logout', url_name='logout')
    def logout(self, request):
        django_logout(request)  # Log out the user
        return Response({'status': 'logout successful'}, status=status.HTTP_200_OK)

    # Retrieve user details
    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            return Response(UserSerializer(user).data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # List all users (Optional)
    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
