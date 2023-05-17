from django.db import models


class Item(models.Model):

    user = models.ForeignKey("PantryUser", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='items')
    price = models.DecimalField(max_digits=10, decimal_places=2)