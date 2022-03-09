from django.db import models


class RentedItem(models.Model):
    renter = models.ForeignKey("Lender", on_delete=models.CASCADE, related_name="renter")
    rental_item = models.ForeignKey("Item", on_delete=models.CASCADE)
    rented_on = models.DateField(auto_now_add=True)
    return_by = models.DateField()