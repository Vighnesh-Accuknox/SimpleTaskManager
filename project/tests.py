from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from .models import User, Project
from rest_framework_simplejwt.tokens import RefreshToken

class ProjectTestCase(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(username="admin1", password='test1234!', email="admin1@gmail.com")
        self.regular_user = User.objects.create_user(username="vasu1", password='test1234!', email="vasu1@gmail.com")
        self.client = APIClient()
        self.project_data = {"project_name": "Test Project"}

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_admin_can_create_project(self):
        self.authenticate(self.admin_user)
        url = reverse('projects-list')
        response = self.client.post(url, self.project_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)

    def test_non_admin_cannot_create_project(self):
        self.authenticate(self.regular_user)
        url = reverse('projects-list')
        response = self.client.post(url, self.project_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)