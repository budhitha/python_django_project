from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from company.models import CarParts


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    created_datetime = models.DateTimeField(default=datetime.now, blank=True)
    updated_datetime = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.user.first_name


class ShoppingCart(models.Model):
    quantity = models.IntegerField(null=False)
    created_datetime = models.DateTimeField(default=datetime.now, blank=True)
    updated_datetime = models.DateTimeField(auto_now=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    car_part = models.ForeignKey(CarParts, on_delete=models.CASCADE, null=True)

    stat = (
        ('Pending', 'Pending'), ('Purchased', 'Purchased'), ('Delivering ', 'Delivering'), ('Delivered', 'Delivered')
    )
    status = models.CharField(max_length=50, choices=stat, default='Pending', null=True)

    delivery_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.quantity
