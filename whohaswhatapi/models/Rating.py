from django.db import models


class Rating(models.Model):
    rater = models.ForeignKey("Lender", on_delete=models.CASCADE, related_name="rater")
    rated = models.ForeignKey("Lender", on_delete=models.CASCADE, related_name="rated")
    rating = models.IntegerField()
    