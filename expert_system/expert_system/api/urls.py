from django.urls import path

from expert_system.data_handler.views import ButtonViewSet, TextViewSet

app_name = 'api'

urlpatterns = [
    path('button/<slug:slug>/', ButtonViewSet.as_view(), name='buttons'),
    path('text/<slug:slug>/', TextViewSet.as_view(), name='texts'),
]
