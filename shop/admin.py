from django.contrib import admin
from .models import Message, Category, SubCategory, Item, Order

# Register your models here.
admin.site.register(Message)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Item)
admin.site.register(Order)