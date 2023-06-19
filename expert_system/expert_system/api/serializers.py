from rest_framework import serializers
from data_handler.models import RequestPosition, RequestStock, RequestRate


class RequestPositionSerializer(serializers.ModelSerializer):
    articul = serializers.IntegerField(
        queryset=RequestPosition.objects.all(),
    )
    text = serializers.CharFieldCharField(
        max_length=255,
        min_length=None,
        allow_blank=False,
        trim_whitespace=True)

    class Meta:
        model = RequestPosition
        fields = ('articul', 'text')
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('articul', 'text'),
                message=("Такая позиция уже существует.")
            ),
        )


class RequestStockSerializer(serializers.ModelSerializer):
    articul = serializers.IntegerField(
        queryset=RequestStock.objects.all(),
    )

    class Meta:
        model = RequestStock
        fields = ('articul')
        validators = (
            serializers.UniqueValidator(
                queryset=model.objects.all(),
                fields=('articul'),
                message=("Такой артикул уже существует.")
            ),
        )


class RequestRateSerializer(serializers.ModelSerializer):
    warehouse_id = serializers.IntegerField(
        queryset=RequestRate.objects.all(),
    )

    class Meta:
        model = RequestRate
        fields = ('warehouse_id')
        validators = (
            serializers.UniqueValidator(
                queryset=model.objects.all(),
                fields=('warehouse_id'),
                message=(
                    "Такой ключ (warehouse_id) уже существует.")
            ),
        )
