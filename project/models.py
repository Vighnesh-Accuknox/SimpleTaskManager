from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError("The Username is required")
        if not email:
            raise ValueError("The Email is required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username} -- {self.email}"
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser    

    
class Project(models.Model):
    project_name = models.CharField(null=False, max_length=256, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin")

    def __str__(self):
        return f"{self.project_name} - {self.created_by.username}"
    
class StatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    ONGOING = 'ongoing', 'ongoing'
    COMPLETED = 'completed', 'Completed'

class Task(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taskadmin")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="assigned_to")
    title = models.CharField(null=False, max_length=256, unique=True) 
    description = models.CharField(null=False, max_length=256)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        null=False
    )
    deadline = models.DateTimeField(null=False)

    def __str__(self):
        return f"{self.id} - {self.created_by.username} - {self.title}"