from django.db import models

import uuid


class UserConsumerBase(models.Model):
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

    class Meta:
        abstract = True
        db_table = 'user_consumer'
        verbose_name = 'User_consumer'
        verbose_name_plural = 'User_consumer'
