from django.db import models


class List(models.Model):

    user = models.ForeignKey("PantryUser", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    notes = models.CharField(max_length=500, blank=True)
    date_created = models.DateField()
    completed = models.BooleanField(default=False)
    date_completed = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)