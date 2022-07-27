from rest_framework import serializers
from .models import Supply


class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = ('id', 'order_num', 'dollar_cost', 'date_supply', 'ruble_cost')
