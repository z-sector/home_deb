""""Declare models for accounts app."""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import uuid

from .base_models import user_type, profile, terms, group, permission


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not password or not settings.REG_PASSWORD.match(password):
            raise ValueError(
                'Password does not match the pattern. '
                'Must be at least 8 characters, '
                'one lowercase and uppercase letters, '
                'one number and a special character (example, ! @ # $% ^ & *)'
            )
        if not email or not settings.REG_EMAIL.match(email):
            raise ValueError('Email does not match the pattern. ')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', UserType(id=1))

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class GroupUserType(user_type.GroupUserTypeBase):
    pass


class UserType(user_type.UserTypeBase):
    group_user_type = models.ForeignKey(GroupUserType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.group_user_type.name}.{self.name}"


class Group(group.GroupBase):
    pass


class User(AbstractUser):
    """User model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.OneToOneField(UserType, on_delete=models.SET_NULL, blank=True, null=True)
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


class UserConsumer(profile.UserConsumerBase):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True)


class Terms(terms.TermsBase):
    pass


class UserTypeTerms(terms.UserTypeTermsBase):
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    terms = models.ForeignKey(Terms, on_delete=models.CASCADE)


class UserTerms(terms.UserTermsBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type_terms = models.ForeignKey(UserTypeTerms, on_delete=models.CASCADE)


class Permission(permission.PermissionBase):
    pass


class UserTypePermission(permission.UserTypePermissionBase):
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)


class UserPermission(permission.UserPermissionBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type_permission = models.ForeignKey(UserTypePermission, on_delete=models.CASCADE)
