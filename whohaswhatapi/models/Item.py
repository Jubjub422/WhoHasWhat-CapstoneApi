from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=75)
    owner = models.ForeignKey("Lender", on_delete=models.CASCADE)
    price_per_day = models.DecimalField(max_digits=4, decimal_places=2)
    price_per_week = models.DecimalField(max_digits=5, decimal_places=2)
    rented_currently = models.BooleanField(default=False)
    condition = models.ForeignKey(
        "Condition", on_delete=models.SET_NULL, null=True)
    item_image = models.URLField(max_length=400)
    categories = models.ManyToManyField(
        "Category", through="ItemCategory", related_name="categories")
