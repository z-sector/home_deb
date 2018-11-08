from django.db import models

import uuid


class TermsBase(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    date_create = models.DateField(auto_now_add=True)
    date_expire = models.DateField()

    class Meta:
        abstract = True
        db_table = 'terms'
        verbose_name = 'Term'
        verbose_name_plural = 'Terms'


class UserTypeTermsBase(models.Model):
    id = models.IntegerField(primary_key=True)
    acting = models.BooleanField(default=True)

    class Meta:
        abstract = True
        db_table = 'user_type_terms'
        verbose_name = 'User_type_has_term'
        verbose_name_plural = 'User_type_has_term'


class UserTermsBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    confirmed = models.BooleanField(default=False)

    class Meta:
        abstract = True
        db_table = 'user_terms'
        verbose_name = 'User_term'
        verbose_name_plural = 'User_terms'
