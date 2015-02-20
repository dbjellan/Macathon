from django.db import models

class Store(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()


class Product(models.Model):
    measurements = (
        ('OZ', 'Ounces'),
        ('FOZ', 'Fluid Ounces'),
    )

    price = models.DecimalField(decimal_places=2, max_digits=4)
    name = models.TextField()
    description = models.TextField()
    units = models.CharField(max_length=5, choices=measurements)
    quantity = models.FloatField()
    available_stores = models.ManyToManyField(Store)

class List(models.Model):
    products = models.ManyToManyField(Product)
    name = models.TextField()
