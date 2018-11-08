from django.db import models


class GroupUserTypeBase(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        abstract = True
        db_table = 'group_user_type'
        verbose_name = 'Group_user_type'
        verbose_name_plural = 'Group_user_type'


class UserTypeBase(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        abstract = True
        db_table = 'user_type'
        verbose_name = 'User_type'
        verbose_name_plural = 'User_type'
