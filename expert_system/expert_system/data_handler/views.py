from api.serializers import (PositionSubscriptionSerializer,
                             RequestPositionSerializer, RequestRateSerializer,
                             RequestStockSerializer)
from data_handler.models import (PositionSubscription, RequestPosition,
                                 RequestRate, RequestStock)
from rest_framework import generics, viewsets


class RequestPositionViewSet(generics.CreateAPIView):
    """Добавление Position в БД."""
    serializer_class = RequestPositionSerializer
    queryset = RequestPosition.objects.all()


class RequestStockViewSet(generics.CreateAPIView):
    """Добавление Stock в БД."""
    serializer_class = RequestStockSerializer
    queryset = RequestStock.objects.all()


class RequestRateViewSet(generics.CreateAPIView):
    """Добавление Rate в БД."""
    serializer_class = RequestRateSerializer
    queryset = RequestRate.objects.all()


class PositionSubscriptionViewSet(generics.ListCreateAPIView):
    """Добавление Subscription в БД."""
    serializer_class = PositionSubscriptionSerializer
    queryset = PositionSubscription.objects.all()


class GETSubscriptionViewSet(generics.ListAPIView):
    """Возврат Subscription пользователю."""
    serializer_class = PositionSubscriptionSerializer

    def get_queryset(self):
        queryset = PositionSubscription.objects.filter(user_id=self.kwargs.get('user_id'))
        return queryset


# class DELETESubscriptionViewSet(generics.DestroyAPIView):
class DELETESubscriptionViewSet(generics.RetrieveUpdateDestroyAPIView):
    """Удаление Subscription из БД пользователем."""
    serializer_class = PositionSubscriptionSerializer
    
    def get_object(self):
        object = PositionSubscription.objects.get(user_id=self.kwargs.get('user_id'), articul=self.kwargs.get('articul'))
        return object
