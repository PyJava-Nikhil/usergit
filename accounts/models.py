from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import JSONField
# Create your models here.


class AccountManager(BaseUserManager):

    def _create_user(self, login, password, **kwargs):

        user = self.model(login=login, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, login, password = None, **kwargs):

        kwargs.setdefault('is_superuser', False)
        return self._create_user(login, password, **kwargs)

    def create_superuser(self, login, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_active', True)
        return self._create_user(login, password, **kwargs)


class Account(AbstractBaseUser, PermissionsMixin):

    unique_id = models.CharField(max_length=40, unique=True)
    login = models.CharField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_info = JSONField(null=True)
    objects = AccountManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['unique_id', ]

    class Meta:
        ordering = ['-date_added']

    def get_full_name(self):
        return str(self.login)

    def get_short_name(self):
        return str(self.login)


class APIReport(models.Model):

    api_url = models.URLField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)



