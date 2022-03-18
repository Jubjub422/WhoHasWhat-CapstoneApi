from django.db import models


class Condition(models.Model):
    condition = models.CharField(max_length=30)
    description = models.CharField(max_length=150)
