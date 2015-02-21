from django.contrib import admin
from grocerylist.models import List, Product, Store, StoreProduct, ProductOrder

admin.site.register(StoreProduct)
admin.site.register(ProductOrder)
admin.site.register(List)
admin.site.register(Product)
admin.site.register(Store)


