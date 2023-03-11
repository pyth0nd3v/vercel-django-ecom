from django.db import models
from django.contrib.auth.models import User
from PIL import Image



# Create your models here.

class Message(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    message = models.CharField(max_length=2000)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    cat_name = models.CharField(max_length=30)
    cat_image = models.ImageField(upload_to =  'images/categories/')
    cat_desc = models.CharField(max_length=100)
    cat_active = models.BooleanField(default=True)
    cat_created_at = models.DateTimeField(auto_now=True)
    cat_updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cat_name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class SubCategory(models.Model):
    sub_name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='Sub_Category')
    sub_image = models.ImageField(upload_to = 'images/subCategories')
    sub_desc = models.CharField(max_length=100)
    sub_active = models.BooleanField(default=True)
    sub_created_at = models.DateTimeField(auto_now=True)
    sub_updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sub_name

    class Meta:
        verbose_name = 'Sub-Category'
        verbose_name_plural = 'Sub-Categories'

class Item(models.Model):
    item_name = models.CharField(max_length=30)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='item_subCategory')
    item_image = models.ImageField(upload_to = 'images/items')
    item_desc = models.CharField(max_length=100)
    item_price = models.PositiveIntegerField(default = 0)
    item_active = models.BooleanField(default=True)
    item_created_at = models.DateTimeField(auto_now=True)
    item_updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.item_image.path)

        if img.width != 600 and img.height != 748:
            output_size = (600, 748)
            img.thumbnail(output_size)
            img.save(self.item_image.path)


class Order(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=14)
    order_email = models.EmailField(max_length=254)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=150)
    city = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=6)
    order_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='orderItem')
    order_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_by_user')
    # order_quantity = models.PositiveIntegerField(default=0)
    order_price = models.PositiveIntegerField(default=0)
    delivered = models.BooleanField(default=False)
    order_created_at = models.DateTimeField(auto_now=True)
    order_updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_item) + " ==> " + str(self.order_user)
    
    def save(self, *args, **kwargs):
        try:
            self.order_price = self.order_item.item_price
            super().save(*args, **kwargs)
        except: 
            pass