from django.urls import path

from expert_system.data_handler.views import ButtonViewSet, TextViewSet
from expert_system.data_handler.views import (RequestPositionViewSet,
                                              RequestRateViewSet,
                                              RequestStockViewSet)


app_name = "api"

urlpatterns = [
    path("button/<slug:slug>/", ButtonViewSet.as_view(), name="buttons"),
    path("text/<slug:slug>/", TextViewSet.as_view(), name="texts"),
    path("request_position/", RequestPositionViewSet.as_view(),
         name="new_request_position"),
    path("request_stock/", RequestStockViewSet.as_view(),
         name="new_request_stock"),
    path("request_rate/", RequestRateViewSet.as_view(),
         name="new_request_rate"),
]
