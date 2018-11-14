from django.db import models

from apps.user_management.accounts.models import User, UserType


# Create your models here.


class Permission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'permission'
        verbose_name = 'Permission'
        verbose_name_plural = 'Permission'


class UserTypePermissionBase(models.Model):
    id = models.IntegerField(primary_key=True)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_type_permission'
        verbose_name = 'User_type_permission'
        verbose_name_plural = 'User_type_permission'


class UserPermissionBase(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type_permission = models.ForeignKey(UserTypePermissionBase, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_permission'
        verbose_name = 'User_permission'
        verbose_name_plural = 'User_permission'
