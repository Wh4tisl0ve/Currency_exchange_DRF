from django.db import models


class Currency(models.Model):
    Code = models.CharField(max_length=3, unique=True, db_index=True)
    FullName = models.CharField(max_length=20)
    Sign = models.CharField(max_length=3)
