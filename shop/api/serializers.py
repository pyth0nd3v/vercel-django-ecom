from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Message, Category, SubCategory, Item, Order

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['name', 'email', 'message']

class PurchasingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderListSerializer(serializers.ModelSerializer):
    order_item = serializers.StringRelatedField(read_only=True)
    image = serializers.ImageField(source = 'order_item.item_image')
    class Meta:
        model = Order
        fields = ['id', 'delivered', 'order_price', 'order_item', 'image', 'order_updated_at']

    

#----------------- These Serializers for ItemView ----------------------

class CategorySerializer_item(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id', "cat_name"]

class SubCategorySerializer_item(serializers.ModelSerializer):
    category = CategorySerializer_item(read_only=True)

    class Meta:
        model = SubCategory
        fields = ['id', "sub_name", "category"]


class ItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    sub_category = SubCategorySerializer_item(read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'item_name', 'item_desc', 'image_url', 'sub_category', 'item_price']

    def get_image_url(self, obj):
        return 'http://127.0.0.1:8000' + obj.item_image.url

#----------------- END Serializers for ItemView ----------------------

#----------------- These Serializers for CategoryView ----------------------

class ItemSerializer_category_nav(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['item_name', 'image_url']

    def get_image_url(self, obj):
        return 'http://127.0.0.1:8000' + obj.item_image.url


class SubCategorySerializer_category_nav(serializers.ModelSerializer):
    item_subCategory = ItemSerializer_category_nav(many=True, read_only = True)
    class Meta:
        model = SubCategory
        fields = ["sub_name", "category", "item_subCategory"]

class CategorySerializer_nav(serializers.ModelSerializer):
    Sub_Category = SubCategorySerializer_category_nav(many=True, read_only = True)
    class Meta:
        model = Category
        fields = ["cat_name", "Sub_Category"]

#----------------- END Serializers for CategoryView ----------------------


#----------------- These Serializers for CategoryFilterWiseView ----------------------

class ItemSerializer_Filter_Category(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'item_name', 'image_url', 'item_price']

    def get_image_url(self, obj):
        return 'http://127.0.0.1:8000' + obj.item_image.url
    

class CategoryFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "cat_name"]
 

class SubCategorySerializer_category(serializers.ModelSerializer):
    item_subCategory = ItemSerializer_Filter_Category(many=True, read_only = True)
    category = CategoryFilterSerializer(read_only = True)

    class Meta:
        model = SubCategory
        fields = ["category", "sub_name", "item_subCategory"]

#----------------- END Serializers for CategoryFilterWiseView ----------------------
