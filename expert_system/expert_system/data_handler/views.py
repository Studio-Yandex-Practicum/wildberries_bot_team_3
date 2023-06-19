from django.shortcuts import get_object_or_404
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
    serializer_class = RequestPositionSerializer

    def perform_create(self, serializer):
        articul_new = get_object_or_404(
            RequestPosition, articul=self.kwargs.get('articul'))
        text_new = get_object_or_404(
            RequestPosition, text=self.kwargs.get('text'))
        serializer.save(articul=articul_new, text=text_new)


class RequestStockViewSet(generics.CreateAPIView):
    """Добавление Stock в БД
    """
    serializer_class = RequestStockSerializer

    def perform_create(self, serializer):
        articul_new = get_object_or_404(
            RequestStock, articul=self.kwargs.get('articul'))
        serializer.save(articul=articul_new)


class RequestRateViewSet(generics.CreateAPIView):
    """Добавление Rate в БД
    """
    serializer_class = RequestRateSerializer

    def perform_create(self, serializer):
        warehouse_new = get_object_or_404(
            RequestRate, warehouse_id=self.kwargs.get('warehouse_id'))
        serializer.save(warehouse_id=warehouse_new)
