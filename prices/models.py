from django.db import models

'''ORM mapper for MarketData'''
class MarketData(models.Model):
    id = models.AutoField(primary_key=True)
    option = models.CharField(max_length=3)
    delivery_month = models.CharField(max_length=5)
    PV = models.FloatField(max_length=9)
    call_put = models.CharField(max_length=4)
    price = models.FloatField(max_length=9)
    currency_units = models.CharField(max_length=10)

