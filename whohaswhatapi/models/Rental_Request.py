from django.db import models


class RequestQueue(models.Model):
    owner = models.ForeignKey(
        "Lender", on_delete=models.CASCADE, related_name='item_owner')
    renter = models.ForeignKey(
        "Lender", on_delete=models.CASCADE, related_name='item_renter')
    item = models.ForeignKey(
        "Item", on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)
