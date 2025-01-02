from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True, db_index=True)
    fullname = models.CharField(max_length=20)
    sign = models.CharField(max_length=3)
