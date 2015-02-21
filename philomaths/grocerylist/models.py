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
    name = models.TextField()

    def __unicode__(self):
        return self.name

class Product(models.Model):
    measurements = (
        ('OZ', 'Ounces'),
        ('FOZ', 'Fluid Ounces'),
    )

    name = models.TextField()
    description = models.TextField()
    units = models.CharField(max_length=5, choices=measurements)
    quantity = models.FloatField()
    
    def __unicode__(self):
        return self.name

class StoreProduct(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=8)
    product = models.ForeignKey(Product)
    store = models.ForeignKey(Store)

    def __unicode__(self):
        return self.product.name + '    ' + str(self.price)

class ProductOrder(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(Product)

    def __unicode__(self):
        return self.product.name + '    ' + str(self.quantity)


class List(models.Model):
    products = models.ManyToManyField(ProductOrder)
    name = models.TextField()
    uuid = UUIDField(primary_key=True, editable=False)

    def __unicode__(self):
        return self.name

        
