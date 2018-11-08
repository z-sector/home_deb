from django.db import models


class GroupBase(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        abstract = True
        db_table = 'group'
        verbose_name = 'Group'
        verbose_name_plural = 'Group'
