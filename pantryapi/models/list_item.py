from django.db import models
from django.contrib.auth import get_user_model


class ListItem(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    list = models.ForeignKey("List", on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name='lists')
    quantity = models.IntegerField()
    priority = models.BooleanField(default=False)
