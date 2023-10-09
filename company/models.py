from datetime import datetime

from django.db import models
from ckeditor.fields import RichTextField


class CarParts(models.Model):
    year_choice = []
    for r in range(1990, (datetime.now().year + 1)):
        year_choice.append((r, r))

    car_part_title = models.CharField(max_length=255)
    color = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField('year', choices=year_choice)
    condition = models.CharField(max_length=100)
    price = models.IntegerField()
    description = RichTextField()
    specifications = RichTextField()
    imported_country = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    created_datetime = models.DateTimeField(default=datetime.now, blank=True)
    updated_datetime = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.car_part_title
