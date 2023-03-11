from django.urls import path
from .views import MessageView, ItemView, CategoryWiseFilterView, PurchasingView, MyorderView, \
                                ItemViewRetrieve, CategoryView, Index


urlpatterns = [
    
    path('', Index.as_view()),
    path('items/', ItemView.as_view()),
    path('items/<int:pk>/', ItemViewRetrieve.as_view()),
    path('category/', CategoryView.as_view()),
    path('category-filter/', CategoryWiseFilterView.as_view()),
    path('contactus/', MessageView.as_view()),
    path('purchasing/', PurchasingView.as_view()),
    path('invoice/<int:pk>/', MyorderView.as_view()),
    path('myorder/', MyorderView.as_view()),
    path('myorder/<int:pk>/', MyorderView.as_view()),


]