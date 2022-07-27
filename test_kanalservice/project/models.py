from django.db import models


class Supply(models.Model):
    id = models.IntegerField(primary_key=True)
    order_num = models.IntegerField()
    dollar_cost = models.IntegerField()
    date_supply = models.CharField(max_length=100)
    ruble_cost = models.FloatField()
