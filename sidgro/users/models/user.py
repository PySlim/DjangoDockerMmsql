from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from sidgro.utils.models import SidgroModel
from django.contrib.auth.models import AbstractUser


class User(SidgroModel,AbstractUser):
    """Default user for sg-sst."""
    name = models.CharField(max_length=150)
    nickname = models.CharField(max_length=50,unique=True)
    #: First and last name do not cover name patterns around the globe
    active = models.BooleanField('Activo', default=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name','nickname']
    userUpdate= models.BooleanField(default=False)
       
    class Meta(SidgroModel.Meta):
        db_table = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.nickname
