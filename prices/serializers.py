from rest_framework import serializers
from rest_framework.fields import CharField, FloatField
from prices.models import MarketData

'''Serializer class for MarketData object'''
class MarketDataSerializer(serializers.ModelSerializer):
    option = CharField(required=True)
    delivery_month = CharField(required=True)
    call_put = CharField(required=True)
    price = FloatField(required=True)
    currency_units = CharField(required=True)
    PV = FloatField(required=False)

    class Meta:
        model = MarketData
        fields = ['id', 'option', 'delivery_month', 'call_put', 'price', 'currency_units', 'PV']
