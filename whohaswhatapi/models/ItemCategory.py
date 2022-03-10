from django.db import models

class ItemCategory(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)