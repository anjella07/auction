from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import *
from .permissions import *
from .filters import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(generics.CreateAPIView):
    serializer_class = UserProfileSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializers
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSimpleSerializers

class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializers
    permission_classes = [UserEdit]

class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializers

class BrandDetailAPIView(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandDetailSerializers

class CarModelListAPIView(generics.ListAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelListSerializers


class CarModelDetailAPIView(generics.RetrieveAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelDetailSerializers

class CarListAPIView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CarFilter
    ordering_fields = ['price']

class CarDetailAPIView(generics.RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarDetailSerializers

class ActionListAPIView(generics.ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionListSerializers

class ActionDetailAPIView(generics.RetrieveAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializers

class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializers

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializers
    permission_classes = [CheckUserBuyer]

class CarCreateApiView(generics.CreateAPIView):
    serializer_class = CarCreateSerializers
    permission_classes = [CheckUserSeller]

class AuctionCreateApiView(generics.CreateAPIView):
    serializer_class = AuctionCreateSerializers
    permission_classes = [CheckUserSeller]

class CarEditApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarCreateSerializers
    permission_classes = [CheckUserSeller, CheckCarEdit]

class AuctionEditApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionCreateSerializers
    permission_classes = [CheckUserSeller, CheckAuctionEdit]