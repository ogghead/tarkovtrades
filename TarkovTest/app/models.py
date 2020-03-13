import datetime

from django.db import models
from django.utils import timezone
import math

# Create your models here.
class Item(models.Model):
    traders = ['Prapor', 'Therapist', 'Fence', 'Skier',
               'Peacekeeper', 'Mechanic', 'Ragman', 'Jaeger']
    traders = [(i, i) for i in traders]
    name = models.CharField(max_length=200)
    highest_sell_price_to_trader = models.IntegerField() # Highest sell price of this item to a trader
    highest_sell_price_trader = models.CharField(choices=traders, max_length=200) # Trader for highest sell price
    lowest_buy_price_from_trader = models.IntegerField(blank=True) # Lowest buy price of this item from a trader, may be blank if not available from traders
    lowest_buy_price_trader = models.CharField(choices=traders, max_length=200, blank=True) # Trader for lowest buy price, may be blank if not available from traders
    market_buy_price = models.IntegerField() # The seen price on the market

    def calculate_fee(self, post_price, intel_center):
        v0 = self.lowest_buy_price_from_trader
        vr = post_price
        ti = tr = 0.025
        p0 = math.log10(v0/vr)
        pr = math.log10(v0/vr)
        fee = v0 * ti * math.pow(4, p0) + vr * tr * math.pow(4, pr)
        if intel_center:
            fee = .7*fee
        return fee

    @property
    def market_sell_price(self):
        return int(self.market_buy_price - self.calculate_fee(self.market_buy_price, intel_center=False))

    @property
    def min_buy_price(self):
        ls = [i for i in [self.market_buy_price, self.lowest_buy_price_from_trader] if i is not False]
        return min(ls)

    @property
    def max_sell_price(self):
        ls = [i for i in [self.market_sell_price, self.highest_sell_price_to_trader]]
        return max(ls)

    def __unicode__(self):
        """Returns a string representation of an item."""
        return self.name

    def __str__(self):
        return self.name


class Trade(models.Model):
    traders = ['Prapor', 'Therapist', 'Fence', 'Skier',
               'Peacekeeper', 'Mechanic', 'Ragman', 'Jaeger']
    trader = models.CharField(choices=[(i, i) for i in traders], max_length=200)
    input_items = models.ManyToManyField(Item, through='InputCount', related_name='inputs')
    output_items = models.ManyToManyField(Item, through='OutputCount', related_name='outputs')


# class Count(models.Model):
#     item = models.ForeignKey(Item, on_delete=models.PROTECT)
#     trade = models.ForeignKey(Trade, on_delete=models.PROTECT)
#     amount = models.IntegerField()

class InputCount(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    trade = models.ForeignKey(Trade, on_delete=models.PROTECT)
    amount = models.IntegerField()

class OutputCount(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    trade = models.ForeignKey(Trade, on_delete=models.PROTECT)
    amount = models.IntegerField()
