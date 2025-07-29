from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from . import models

class RegistrationSerializer(serializers.ModelSerializer):
    password_2 = serializers.CharField(
        write_only = True,
        required = True
    )
    class Meta:
        model = models.CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_2']

    def create(self, validated_data):
        validated_data.pop('password_2')
        
        user = self.Meta.model.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user

class RegistrationView(APIView):
    def get(self, request):
        return Response("Registration(GET)")
    
    def post(self, request):
        serializer = RegistrationSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response("Registration successful")
        
        return Response(serializer.errors)
    
class LoginView(APIView):
    def get(self, request):
        return Response("Login(GET)")
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response("Username and password are required")

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            return Response("Login successful")
        
        return Response("Something went wrong")

@api_view(['POST'])   
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response("Logout successful")