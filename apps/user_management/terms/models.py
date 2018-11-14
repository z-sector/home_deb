from django.db import models

import uuid

from apps.user_management.accounts.models import UserType, User


# Create your models here.


class Terms(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    date_create = models.DateField(auto_now_add=True)
    date_expire = models.DateField()

    class Meta:
        db_table = 'terms'
        verbose_name = 'Term'
        verbose_name_plural = 'Terms'


class UserTypeTerms(models.Model):
    id = models.IntegerField(primary_key=True)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    terms = models.ForeignKey(Terms, on_delete=models.CASCADE)
    acting = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_type_terms'
        verbose_name = 'User_type_has_term'
        verbose_name_plural = 'User_type_has_term'


class UserTerms(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type_terms = models.ForeignKey(UserTypeTerms, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_terms'
        verbose_name = 'User_term'
        verbose_name_plural = 'User_terms'
