from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'tasks', views.TaskViewSet)
urlpatterns = [
    path("signup", views.UserCreateView.as_view(), name="signup"),
    path("login", views.CheckUserView.as_view(), name="login"),
    path('', include(router.urls)),
]