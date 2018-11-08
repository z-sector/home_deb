""""Declare models for accounts app."""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

import uuid

from .base_models import user_type, profile, terms, group, permission


# USER_TYPE = (
#     (1, 'consumers'),
#     (2, 'organizations'),
#     (3, 'regulators')
# )


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
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

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class GroupUserType(user_type.GroupUserTypeBase):
    pass


class UserType(user_type.UserTypeBase):
    group_user_type_id = models.ForeignKey(GroupUserType, on_delete=models.CASCADE)
    pass


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
    group_id = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True)
    question_1 = models.CharField(max_length=254, null=True, blank=True)
    answer_1 = models.CharField(max_length=254, null=True, blank=True)
    question_2 = models.CharField(max_length=254, null=True, blank=True)
    answer_2 = models.CharField(max_length=254, null=True, blank=True)
    question_3 = models.CharField(max_length=254, null=True, blank=True)
    answer_3 = models.CharField(max_length=254, null=True, blank=True)
    # term_1 = models.BooleanField(default=False)
    # term_2 = models.BooleanField(default=False)
    # term_3 = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = 'user'


class UserConsumer(profile.UserConsumerBase):
    user_id = models.OneToOneField(UserType, on_delete=models.CASCADE, primary_key=True)


class Terms(terms.TermsBase):
    pass


class UserTypeTerms(terms.UserTypeTermsBase):
    user_type_id = models.ForeignKey(UserType, on_delete=models.CASCADE)
    terms_id = models.ForeignKey(Terms, on_delete=models.CASCADE)


class UserTerms(terms.UserTermsBase):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type_terms_id = models.ForeignKey(UserTypeTerms, on_delete=models.CASCADE)


class Permission(permission.PermissionBase):
    pass


class UserTypePermission(permission.UserTypePermissionBase):
    user_type_id = models.ForeignKey(UserType, on_delete=models.CASCADE)
    permission_id = models.ForeignKey(Permission, on_delete=models.CASCADE)


class UserPermission(permission.UserPermissionBase):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type_permission_id = models.ForeignKey(UserTypePermission, on_delete=models.CASCADE)
