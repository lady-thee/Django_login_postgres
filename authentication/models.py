from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
import uuid



class UserManager(BaseUserManager):
    def create_user(self, email, **kwargs):
        if not email:
            raise ValueError('Email must be given')
        kwargs.setdefault('is_superuser', False)
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_staff', False)

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password, **kwargs):
         if not email:
            raise ValueError('Email must be given')
         kwargs.setdefault('is_superuser', True)
         kwargs.setdefault('is_active', True)
         kwargs.setdefault('is_staff', True)

         superuser = self.model(email=self.normalize_email(email),  **kwargs)
         superuser.set_password(password)
         superuser.save(using=self._db)
         return superuser
        
        


class Users(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    email = models.EmailField(max_length=250, unique=True, db_index=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    last_login = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False)

    class Meta:
        unique_together = ['id', 'email']
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email 
    
    def has_perms(self, perm, obj=None):
        return self.is_superuser
    
    def get_full_name(self):
        return self.email
    
    def has_module_perms(self, app_label):
        return True
    
    

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    fullname = models.CharField(max_length=250, null=True, blank=True)
    birthday = models.DateField(help_text='birthday')

    def __str__(self):
        return str(self.fullname)




