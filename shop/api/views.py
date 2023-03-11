from rest_framework.views import APIView
from rest_framework import generics, viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token  

from rest_framework.permissions import IsAuthenticated, AllowAny


from .serializers import MessageSerializer, ItemSerializer,\
                            PurchasingSerializer, OrderListSerializer, \
                                SubCategorySerializer_category, CategorySerializer_nav
from ..models import Message, Category, SubCategory, Item, Order

class MessageView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Item.objects.all().order_by('?')
    serializer_class = ItemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['item_name']

class ItemViewRetrieve(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    def retrieve(self, request, pk=None):
        queryset = Item.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ItemSerializer(user)
        return Response(serializer.data)
    
class CategoryView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer_nav

class CategoryWiseFilterView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer_category
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__cat_name', 'sub_name']

    def get_queryset(self):
        cat_name = self.request.query_params.get('category__cat_name') # get the Category filter parameter
        sub_name = self.request.query_params.get('sub_name') # get the subcategory filter parameter
        queryset = SubCategory.objects.all()
        queryset = queryset.filter(sub_name=sub_name, category__cat_name=cat_name)
        return queryset

class PurchasingView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = (request.data).copy()
        data['order_user'] = request.user.id
        serializer = PurchasingSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class MyorderView(generics.ListCreateAPIView, generics.DestroyAPIView, generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(order_user=user)
    
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if   pk:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def delete(self, *args, **kwargs):
        id = kwargs.get('pk')
        try:
            instance = Order.objects.get(pk=id)
            if instance.delivered == False:
                instance.delete()
                return Response('Your order has been deleted', status=status.HTTP_200_OK )
            else:
                return Response("Sorry! Your order has been delivered, Now order cannot be delete", status=status.HTTP_403_FORBIDDEN )
        except:
            return Response("ID cannot found!", status=status.HTTP_400_BAD_REQUEST )

