import datetime
import math

from django.db import models
from django.utils import timezone

# Create your models here.
class Item(models.Model):
    traders = ['', 'Prapor', 'Therapist', 'Fence', 'Skier',
               'Peacekeeper', 'Mechanic', 'Ragman', 'Jaeger']
    traders = [(i, i) for i in traders]
    name = models.CharField(max_length=200)
    true_value = models.IntegerField()
    highest_sell_price_to_trader = models.IntegerField() # Highest sell price of this item to a trader
    highest_sell_price_trader = models.CharField(choices=traders, max_length=200) # Trader for highest sell price
    lowest_buy_price_from_trader = models.IntegerField(blank=True, null=True) # Lowest buy price of this item from a trader, may be blank if not available from traders
    lowest_buy_price_trader = models.CharField(choices=traders, max_length=200, default=traders[0], blank=True) # Trader for lowest buy price, may be blank if not available from traders
    market_buy_price = models.IntegerField() # The seen price on the market

    def fee(self, intel_center):
        v0 = self.true_value
        vr = self.market_buy_price
        ti = tr = 0.025
        p0 = math.log10(v0/vr)
        pr = math.log10(vr/v0)
        fee = v0 * ti * math.pow(4, p0) + vr * tr * math.pow(4, pr)
        if intel_center:
            fee = .7*fee
        return fee

    @property
    def fee_to_post_at_buy_price_no_intel(self):
        return int(self.fee(False))

    @property
    def fee_to_post_at_buy_price_intel(self):
        return int(self.fee(True))

    @property
    def market_sell_price_no_intel(self):
        return int(self.market_buy_price - self.fee_to_post_at_buy_price_no_intel)

    @property
    def market_sell_price_intel(self):
        return int(self.market_buy_price - self.fee_to_post_at_buy_price_intel)

    @property
    def min_buy_price(self):
        ls = [i for i in [self.market_buy_price, self.lowest_buy_price_from_trader] if i is not None]
        return min(ls)

    @property
    def max_sell_price_no_intel(self):
        ls = [i for i in [self.market_sell_price_no_intel, self.highest_sell_price_to_trader]]
        return max(ls)

    @property
    def max_sell_price_intel(self):
        ls = [i for i in [self.market_sell_price_intel, self.highest_sell_price_to_trader]]
        return max(ls)

    def __unicode__(self):
        """Returns a string representation of an item."""
        return self.name

    def __str__(self):
        return self.name

    #fee_to_post_at_buy_price_no_intel = models.IntegerField(blank=True)
    #fee_to_post_at_buy_price_intel = models.IntegerField(blank=True)

    #def clean(self):
    #    if not self.fee_to_post_at_buy_price_no_intel and not self.fee_to_post_at_buy_price_intel:  # This will check for None or Empty
    #        raise ValidationError({'fee_to_post_at_buy_price_no_intel': _('One of fee_to_post_at_buy_price_no_intel or fee_to_post_at_buy_price_intel should have a value.')})
    #    if not self.fee_to_post_at_buy_price_no_intel:
    #        self.fee_to_post_at_buy_price_no_intel = int(self.fee_to_post_at_buy_price_intel / 0.7)
    #    else:
    #        self.fee_to_post_at_buy_price_intel = int(self.fee_to_post_at_buy_price_no_intel * 0.7)

    #@property
    #def true_value(self):
    #    fee = self.fee_to_post_at_buy_price_no_intel
    #    vr = self.market_buy_price
    #    return (-40 - vr + 40*fee)

class Trade(models.Model):
    traders = ['Prapor', 'Therapist', 'Fence', 'Skier',
               'Peacekeeper', 'Mechanic', 'Ragman', 'Jaeger']
    traders = [(i, i) for i in traders]
    levels = [('I', 1), ('II', 2), ('III', 3), ('Max', 4)]
    trader = models.CharField(choices=traders, max_length=200)
    trader_level = models.CharField(choices=levels, max_length=200)
    input_items = models.ManyToManyField(Item, through='InputCount', related_name='inputs')
    output_items = models.ManyToManyField(Item, through='OutputCount', related_name='outputs')

    @property
    def inputs_sell_price_no_intel(self):
        return sum([i.amount * i.item.max_sell_price_no_intel for i in self.input_items.all()])

    @property
    def inputs_sell_price_intel(self):
        return sum([i.amount * i.item.max_sell_price_intel for i in self.input_items.all()])

    @property
    def outputs_sell_price_no_intel(self):
        return sum([i.amount * i.item.max_sell_price_no_intel for i in self.output_items.all()])

    @property
    def outputs_sell_price_intel(self):
        return sum([i.amount * i.item.max_sell_price_intel for i in self.output_items.all()])


class InputCount(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.item.name} {self.amount}"

class OutputCount(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.item.name} {self.amount}"

#class TrueValueCalc(models.Model):
#    previous_stash = models.IntegerField()
#    cashback = models.IntegerField()
#    new_stash = models.IntegerField()

#    @property
#    def true_value(self):
#        return self.previous_stash + self.cashback - self.new_stash