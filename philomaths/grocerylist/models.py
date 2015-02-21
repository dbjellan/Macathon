from django.db import models
import uuid

class UUIDField(models.CharField) :
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 64 )
        kwargs['blank'] = True
        models.CharField.__init__(self, *args, **kwargs)
    
    def pre_save(self, model_instance, add):
        if add :
            value = str(uuid.uuid4())
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(models.CharField, self).pre_save(model_instance, add)

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
    
    def __unicode__(self):
        return self.name


class List(models.Model):
    products = models.ManyToManyField(Product)
    name = models.TextField()
    uuid = UUIDField(primary_key=True, editable=False)