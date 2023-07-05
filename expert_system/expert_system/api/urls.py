from data_handler.views import (DELETESubscriptionViewSet,
                                GETSubscriptionViewSet,
                                PositionSubscriptionViewSet,
                                RequestPositionViewSet, RequestRateViewSet,
                                RequestStockViewSet)
from django.urls import path

app_name = "api"

urlpatterns = [
    path("request_position/", RequestPositionViewSet.as_view(),
         name="new_request_position"),
    path("request_stock/", RequestStockViewSet.as_view(),
         name="new_request_stock"),
    path("request_rate/", RequestRateViewSet.as_view(),
         name="new_request_rate"),
    path("position_subscription/", PositionSubscriptionViewSet.as_view(),
         name="new_position_subscription"),
    path("position_subscription/<int:user_id>", GETSubscriptionViewSet.as_view(),
         name="get_subscriptions"),
    path("position_subscription/<int:user_id>/<int:articul>", DELETESubscriptionViewSet.as_view(),
         name="delete_subscriptions"),
]
