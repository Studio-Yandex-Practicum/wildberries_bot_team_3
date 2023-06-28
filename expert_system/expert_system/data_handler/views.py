from rest_framework import generics

from api.serializers import (RequestPositionSerializer,
                             RequestRateSerializer,
                             RequestStockSerializer)
from data_handler.models import RequestPosition, RequestRate, RequestStock


class ButtonViewSet(generics.RetrieveAPIView):
    pass


class TextViewSet(generics.RetrieveAPIView):
    pass


class RequestPositionViewSet(generics.CreateAPIView):
    """Добавление Position в БД
    """
    queryset = RequestPosition.objects.all()
    serializer_class = RequestPositionSerializer
    if serializer_class.is_valid:
        serializer_class.save()


class RequestStockViewSet(generics.CreateAPIView):
    """Добавление Stock в БД
    """
    queryset = RequestStock.objects.all()
    serializer_class = RequestStockSerializer
    if serializer_class.is_valid:
        serializer_class.save()


class RequestRateViewSet(generics.CreateAPIView):
    """Добавление Rate в БД
    """
    queryset = RequestRate.objects.all()
    serializer_class = RequestRateSerializer
    if serializer_class.is_valid:
        serializer_class.save()
