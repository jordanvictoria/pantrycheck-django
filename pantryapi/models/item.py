from django.db import models
from django.contrib.auth import get_user_model


class Item(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='items')
    price = models.DecimalField(max_digits=10, decimal_places=2)