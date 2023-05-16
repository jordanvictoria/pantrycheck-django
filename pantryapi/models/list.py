from django.db import models
from django.contrib.auth import get_user_model


class List(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    notes = models.CharField(max_length=500)
    date_created = models.DateField()
    completed = models.BooleanField(default=False)
    date_completed = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)