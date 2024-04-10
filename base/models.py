from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    image = models.ImageField(upload_to="static/cars")
    name = models.CharField( max_length=50)
    price = models.IntegerField()
    posted = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    speed = models.IntegerField()
    def __str__(self):
        return self.name

class Order(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")
    is_active = models.BooleanField(default = False)
    def __str__(self):
        return str(self.date)

