from rest_framework import serializers
from data_handler.models import RequestPosition, RequestStock, RequestRate


class RequestPositionSerializer(serializers.ModelSerializer):
    articul = serializers.IntegerField()
    text = serializers.CharField(
        max_length=255,
        min_length=None,
        allow_blank=False,
        trim_whitespace=True)

    class Meta:
        model = RequestPosition
        fields = ('articul', 'text')

        def validate(self, attrs):
            if RequestPosition.objects.filter(**attrs).exists():
                raise serializers.ValidationError(
                    "Такая позиция уже существует.")
            return attrs

    def create(self, validated_data):
        return RequestPosition.objects.create(**validated_data)


class RequestStockSerializer(serializers.ModelSerializer):
    articul = serializers.IntegerField()

    class Meta:
        model = RequestStock
        fields = ('articul')

        def validate(self, attrs):
            if RequestStock.objects.filter(**attrs).exists():
                raise serializers.ValidationError(
                    "Такой артикул уже существует.")
            return attrs

    def create(self, validated_data):
        return RequestStock.objects.create(**validated_data)


class RequestRateSerializer(serializers.ModelSerializer):
    warehouse_id = serializers.IntegerField()

    class Meta:
        model = RequestRate
        fields = ('warehouse_id')

        def validate(self, attrs):
            if RequestRate.objects.filter(**attrs).exists():
                raise serializers.ValidationError(
                    "Такой ключ (warehouse_id) уже существует.")
            return attrs

    def create(self, validated_data):
        return RequestRate.objects.create(**validated_data)
