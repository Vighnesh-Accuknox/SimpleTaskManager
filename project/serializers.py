from rest_framework import serializers
from .models import User, Project, Task
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer): #for User Signup
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
class CheckUserSerializer(serializers.ModelSerializer): #for User Login
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

class TaskSerializer(serializers.ModelSerializer): #for Tasks 
    
    class Meta:
        model = Task
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer): #for Project
    created_by = serializers.ReadOnlyField(source='created_by.id')
    tasks = TaskSerializer(many=True, read_only=True, source='assigned_to')
    class Meta:
        model = Project
        fields = '__all__'


