from django.db import models
from django.contrib.auth.models import User

class Lender(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=125)
    email = models.EmailField(max_length=250)
    is_owner = models.BooleanField(default=False)
    is_renter = models.BooleanField(default = True)
    profile_image_url = models.URLField(max_length=500)