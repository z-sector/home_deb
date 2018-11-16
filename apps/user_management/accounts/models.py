""""Declare models for accounts app."""

# from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import uuid


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not settings.REG_PASSWORD.match(password):
            raise ValueError(
                'Password does not match the pattern. '
                'Must be at least 12 characters, '
                'two lowercase and uppercase letters, '
                'two number and one special character (example, ! @ # $% ^ & *)'
            )

        if not settings.REG_USER_NAME.match(username):
            raise ValueError('Username does not match the pattern.')
        if not settings.REG_EMAIL.match(email):
            raise ValueError('Email does not match the pattern.')

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self,username, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        # extra_fields.setdefault('is_staff', False)
        # extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', UserType(id=1))

        # if extra_fields.get('is_staff') is not True:
        #     raise ValueError('Superuser must have is_staff=True.')
        # if extra_fields.get('is_superuser') is not True:
        #     raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class GroupUserType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'group_user_type'
        verbose_name = 'Group_user_type'
        verbose_name_plural = 'Group_user_type'


class UserType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    group_user_type = models.ForeignKey(GroupUserType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.group_user_type.name}.{self.name}"

    class Meta:
        db_table = 'user_type'
        verbose_name = 'User_type'
        verbose_name_plural = 'User_type'


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'group'
        verbose_name = 'Group'
        verbose_name_plural = 'Group'


class User(AbstractBaseUser):
    """User model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(_('email address'))
    is_active = models.BooleanField(_('active'), default=True)
    user_type = models.ForeignKey(UserType, on_delete=models.SET_NULL, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True)
    question_1 = models.CharField(max_length=254, null=True, blank=True)
    answer_1 = models.CharField(max_length=254, null=True, blank=True)
    question_2 = models.CharField(max_length=254, null=True, blank=True)
    answer_2 = models.CharField(max_length=254, null=True, blank=True)
    question_3 = models.CharField(max_length=254, null=True, blank=True)
    answer_3 = models.CharField(max_length=254, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __iter__(self):
        for field_name in self._meta.local_fields:
            value = getattr(self, field_name.name, None)
            if value is not None:
                yield (field_name.name, value.__str__())

    class Meta:
        db_table = 'user'
        verbose_name = 'user'


class UserConsumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True)
    salutation = models.CharField(max_length=30, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    last_nam = models.CharField(max_length=30, null=True, blank=True)
    suffix = models.CharField(max_length=30, null=True, blank=True)
    ssn = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=254, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    zip = models.CharField(max_length=30, null=True, blank=True)
    phone_1 = models.CharField(max_length=30, null=True, blank=True)
    phone_2 = models.CharField(max_length=30, null=True, blank=True)
    phone_3 = models.CharField(max_length=30, null=True, blank=True)
    question_1 = models.CharField(max_length=254, null=True, blank=True)
    answer_1 = models.CharField(max_length=254, null=True, blank=True)
    question_2 = models.CharField(max_length=254, null=True, blank=True)
    answer_2 = models.CharField(max_length=254, null=True, blank=True)
    question_3 = models.CharField(max_length=254, null=True, blank=True)
    answer_3 = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        db_table = 'user_consumer'
        verbose_name = 'User_consumer'
        verbose_name_plural = 'User_consumer'
