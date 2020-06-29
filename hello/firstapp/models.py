from django.db import models


class SortedFile(models.Model):
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    group = models.CharField(max_length=200)
    number = models.CharField(max_length=200)
    group_ref = models.CharField(max_length=200)
    info = models.CharField(max_length=1200)
