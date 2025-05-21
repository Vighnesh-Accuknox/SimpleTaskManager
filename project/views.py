from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import User, Project, Task
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer, CheckUserSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken  
from django.contrib.auth.hashers import check_password
from .filters import TaskFilter
from django_filters.rest_framework import DjangoFilterBackend

class UserCreateView(APIView):
    permission_classes=[AllowAny]
    def post(self, req):
        serializer = UserSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckUserView(APIView):
    permission_classes=[AllowAny]
    def post(self, req):
        serializer = CheckUserSerializer(data=req.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            # print(username, password)
            user = User.objects.get(username=username)
            print(user)
            if user is not None and check_password(password, user.password):
                token = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login Successful',
                    'access': str(token.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)