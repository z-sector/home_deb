from django.db import models


class PermissionBase(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        abstract = True
        db_table = 'permission'
        verbose_name = 'Permission'
        verbose_name_plural = 'Permission'


class UserTypePermissionBase(models.Model):
    id = models.IntegerField(primary_key=True)

    class Meta:
        abstract = True
        db_table = 'user_type_permission'
        verbose_name = 'User_type_permission'
        verbose_name_plural = 'User_type_permission'


class UserPermissionBase(models.Model):
    id = models.IntegerField(primary_key=True)

    class Meta:
        abstract = True
        db_table = 'user_permission'
        verbose_name = 'User_permission'
        verbose_name_plural = 'User_permission'
