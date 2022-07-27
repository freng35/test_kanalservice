import datetime
import collections
from django.shortcuts import render
from .models import *
from .serializers import SupplySerializer
from rest_framework import generics
from json import dumps


def index(request):
    supply_item = Supply.objects.all()

    supplies = {}
    total_cost = 0
    for item in supply_item:
        total_cost += item.dollar_cost
        if supplies.get(datetime.datetime.strptime(item.date_supply, "%Y-%m-%d"), None):
            supplies[datetime.datetime.strptime(item.date_supply, "%Y-%m-%d")] += item.dollar_cost
        else:
            supplies[datetime.datetime.strptime(item.date_supply, "%Y-%m-%d")] = item.dollar_cost

    sorted_supply = []
    for key in sorted(supplies.keys()):
        sorted_supply.append((key.date().strftime("%Y-%m-%d"), supplies[key]))

    context = {
        'supply': supply_item,
        'total_cost': total_cost,
        'ordered_supply': dumps(sorted_supply)
    }
    return render(request, 'index.html', context)


class SupplyListCreate(generics.ListCreateAPIView):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer
