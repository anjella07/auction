from .views import *
from rest_framework import routers
from django.urls import path, include

router = routers.SimpleRouter()
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'bid', BidViewSet, basename='bid')

urlpatterns = [
    path('', include(router.urls)),
    path('', CarListAPIView.as_view(), name='car_list'),
    path('<int:pk>/', CarDetailAPIView.as_view(), name='car_detail'),
    path('car/create/', CarCreateApiView.as_view(), name='car_create'),
    path('car/create/<int:pk>', CarEditApiView.as_view(), name='car_edit'),
    path('brand/', BrandListAPIView.as_view(), name='brand_list'),
    path('brand/<int:pk>', BrandDetailAPIView.as_view(), name='brand_detail'),
    path('carmodel/', CarModelListAPIView.as_view(), name='carmodel_list'),
    path('carmodel/<int:pk>', CarModelDetailAPIView.as_view(), name='carmodel_detail'),
    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('auction/', ActionListAPIView.as_view(), name='auction_list'),
    path('auction/<int:pk>', ActionDetailAPIView.as_view(), name='auction_detail'),
    path('auction/create/', AuctionCreateApiView.as_view(), name='auction_create'),
    path('auction/create/<int:pk>', AuctionEditApiView.as_view(), name='auction_edit'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
