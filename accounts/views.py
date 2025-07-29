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