import datetime
import math

from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.core.exceptions import ValidationError

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=200, unique=True) # Item names must be unique
    
    sell_traders = ['Therapist', 'Skier', 'Mechanic']
    sell_traders = [(i, i) for i in sell_traders]
    highest_sell_price_to_trader = models.IntegerField() # Highest sell price of this item to a trader
    highest_sell_price_trader = models.CharField(choices=sell_traders, max_length=200) # Trader for highest sell price
    buy_traders = ['', 'Prapor', 'Therapist', 'Fence', 'Skier',
                   'Peacekeeper', 'Mechanic', 'Ragman', 'Jaeger']
    buy_traders = [(i, i) for i in buy_traders]
    lowest_buy_price_from_trader = models.IntegerField(blank=True, null=True) # Lowest buy price of this item from a trader, may be blank if not available from traders
    lowest_buy_price_trader = models.CharField(choices=buy_traders, max_length=200, default=buy_traders[0], blank=True) # Trader for lowest buy price, may be blank if not available from traders
    market_buy_price = models.IntegerField() # The seen price on the market
    # weight = models.FloatField()
    # slots = models.IntegerField()
    # TODO 
    # Implement weights, sizes, any other useful variables and calculated variables
    # Look into making subclasses for ammo, containers, armor, etc.
    # Improve front end design


    def price_validator(self, field, price):
       if price < 0:
           raise ValidationError({field: 'Price cannot be a negative number'})
       elif price == 0:
           raise ValidationError({field: 'Price cannot be zero'})
       elif price > 100000000:
           raise ValidationError({field: 'Price cannot be greater than 100 million'})

    def clean(self):
        # Price validate trader sell price
        self.price_validator('highest_sell_price_to_trader', self.highest_sell_price_to_trader)

        # Price validate trader buy price if it exists
        if self.lowest_buy_price_from_trader:
            self.price_validator('lowest_buy_price_from_trader', self.lowest_buy_price_from_trader)

        # Price validate market price
        self.price_validator('market_buy_price', self.market_buy_price)

    @cached_property
    def true_value(self):
        if self.highest_sell_price_trader == 'Therapist':
            return int(1.333333 * self.highest_sell_price_to_trader)
        elif self.highest_sell_price_trader == 'Skier':
            return int(1.492668 * self.highest_sell_price_to_trader)
        elif self.highest_sell_price_trader == 'Mechanic':
            return int(1.755355 * self.highest_sell_price_to_trader)

    def fee(self):
        '''
        The market fee for an item based on equation found at https://escapefromtarkov.gamepedia.com/Trading
        '''
        v0 = self.true_value
        vr = self.market_buy_price
        ti = tr = 0.025
        p0 = math.log10(v0/vr)
        pr = math.log10(vr/v0)
        fee = v0 * ti * math.pow(4, p0) + vr * tr * math.pow(4, pr)
        return fee

    @cached_property
    def related_input_trades(self):
        '''
        Returns trades for which this item is an input
        '''
        return [i.trade for i in self.inputcount_set.all()]

    @cached_property
    def related_output_trades(self):
        '''
        Returns trades for which this item is an output
        '''
        return [i.trade for i in self.outputcount_set.all()]

    @cached_property
    def fee_to_post_at_buy_price_no_intel(self):
        '''
        Returns calculated market fee for given market price
        '''
        return int(self.fee())

    @cached_property
    def fee_to_post_at_buy_price_intel(self):
        '''
        Returns calculated market fee for given market price, reduced by 30% since intel center is enabled
        '''
        return int(.7*self.fee_to_post_at_buy_price_no_intel)

    @cached_property
    def market_sell_price_no_intel(self):
        '''
        Returns market sell price with no intel center (given market price - fee)
        '''
        return int(self.market_buy_price - self.fee_to_post_at_buy_price_no_intel)

    @cached_property
    def market_sell_price_intel(self):
        '''
        Returns market sell price with intel center (given market price - fee)
        '''
        return int(self.market_buy_price - self.fee_to_post_at_buy_price_intel)

    def min_output_trade_price_and_source_no_intel(self):
        '''
        Returns minimum cost of an item in terms of input items in trades for which this item is an output.
        Value of an output item in terms of input items is calculated as cost of input items * percentage of output value this item is.
        Ex) 500 ruble input value -> 1000 ruble output value with this item as half the output. 500 * .5 = 250 rubles/item.
        '''
        if self.related_output_trades == []: # No related trades, no value in terms of input items
            return (None, None)
        else:
            trades = {}
            for trade in self.related_output_trades: # Get item value of all trades
                if trade.is_useless_no_intel:
                    continue
                trade_inputs_price = trade.inputs_buy_price_no_intel
                trade_outputs_price = trade.outputs_price_no_intel
                percent_of_output_trade = self.max_sell_price_no_intel/trade_outputs_price
                output_item_price = int(percent_of_output_trade*trade_inputs_price)
                trades[output_item_price] = trade
            best_trade_value = min(trades.keys())
            return (best_trade_value, trades[best_trade_value])

    def min_output_trade_price_and_source_intel(self):
        '''
        Returns minimum cost of an item in terms of input items in trades for which this item is an output.
        Value of an output item in terms of input items is calculated as cost of input items * percentage of output value this item is.
        Ex) 500 ruble input value -> 1000 ruble output value with this item as half the output. 500 * .5 = 250 rubles/item.
        '''
        if self.related_output_trades == []: # No related trades, no value in terms of input items
            return (None, None)
        else:
            trades = {}
            for trade in self.related_output_trades: # Get item value of all trades
                if trade.is_useless_intel:
                    continue
                trade_inputs_price = trade.inputs_buy_price_intel
                trade_outputs_price = trade.outputs_price_intel
                percent_of_output_trade = self.max_sell_price_intel/trade_outputs_price
                output_item_price = int(percent_of_output_trade*trade_inputs_price)
                trades[output_item_price] = trade
            best_trade_value = min(trades.keys())
            return (best_trade_value, trades[best_trade_value])
    
    @cached_property
    def no_intel_buy_prices(self):
        '''
        Returns a dictionary of {buy_price: buy_source}
        '''
        min_item_trade_price_no_intel, min_item_trade_source_no_intel = self.min_output_trade_price_and_source_no_intel()
        buy_prices = {self.market_buy_price: 'Market', min_item_trade_price_no_intel: min_item_trade_source_no_intel, self.lowest_buy_price_from_trader: self.lowest_buy_price_trader}
        return buy_prices

    @cached_property
    def intel_buy_prices(self):
        '''
        Returns a dictionary of {buy_price: buy_source}
        '''
        min_item_trade_price_intel, min_item_trade_source_intel = self.min_output_trade_price_and_source_intel()
        buy_prices = {self.market_buy_price: 'Market', min_item_trade_price_intel: min_item_trade_source_intel, self.lowest_buy_price_from_trader: self.lowest_buy_price_trader}
        return buy_prices

    @cached_property
    def min_buy_price_no_intel(self):
        '''
        Returns the best buy price for this item, selected out of trades where this item is an output, traders, and the market.
        '''
        best_buy_price_no_intel = min([i for i in self.no_intel_buy_prices.keys() if i is not None])
        return best_buy_price_no_intel

    @cached_property
    def min_buy_price_intel(self):
        '''
        Returns the best buy price for this item, selected out of trades where this item is an output, traders, and the market.
        '''
        best_buy_price_intel = min([i for i in self.intel_buy_prices.keys() if i is not None])
        return best_buy_price_intel
    
    @cached_property
    def min_buy_price_no_intel_source(self):
        '''
        Returns the source of the best buy price for this item, selected out of trades where this item is an output, traders, and the market
        '''
        return self.no_intel_buy_prices[self.min_buy_price_no_intel]

    @cached_property
    def min_buy_price_no_intel_source_is_trade(self):
        '''
        Returns whether the source of the best buy price for this item is a trade
        '''
        if type(self.min_buy_price_no_intel_source) == str:
            return False
        return True

    @cached_property
    def min_buy_price_intel_source(self):
        '''
        Returns the source of the best buy price for this item, selected out of trades where this item is an output, traders, and the market
        '''
        return self.intel_buy_prices[self.min_buy_price_intel]

    @cached_property
    def min_buy_price_intel_source_is_trade(self):
        '''
        Returns whether the source of the best buy price for this item is a trade
        '''
        if type(self.min_buy_price_intel_source) == str:
            return False
        return True

    def max_input_trade_price_and_source_no_intel(self):
        '''
        Returns maximum cost of an item in terms of output items in trades for which this item is an input.
        Value of an output item in terms of input items is calculated as cost of output items * percentage of input value this item is.
        Ex) 500 ruble input value -> 1000 ruble output value with this item as half the input. 1000 * .5 = 500 rubles/item.
        '''
        if self.related_input_trades == []: # No related trades, no value in terms of input items
            return (None, None)
        else:
            trades = {}
            for trade in self.related_input_trades: # Get item value of all trades
                if trade.is_useless_no_intel:
                    continue
                trade_inputs_price = trade.inputs_buy_price_no_intel
                trade_outputs_price = trade.outputs_price_no_intel
                percent_of_input_trade = self.min_buy_price_no_intel/trade_inputs_price
                input_item_price = int(percent_of_input_trade*trade_outputs_price)
                trades[input_item_price] = trade
            best_trade_value = max(trades.keys())
            return (best_trade_value, trades[best_trade_value])

    def max_input_trade_price_and_source_intel(self):
        '''
        Returns maximum cost of an item in terms of output items in trades for which this item is an input.
        Value of an output item in terms of input items is calculated as cost of output items * percentage of input value this item is.
        Ex) 500 ruble input value -> 1000 ruble output value with this item as half the input. 1000 * .5 = 500 rubles/item.
        '''
        if self.related_input_trades == []: # No related trades, no value in terms of input items
            return (None, None)
        else:
            trades = {}
            for trade in self.related_input_trades: # Get item value of all trades
                if trade.is_useless_intel:
                    continue
                trade_inputs_price = trade.inputs_buy_price_intel
                trade_outputs_price = trade.outputs_price_intel
                percent_of_input_trade = self.min_buy_price_intel/trade_inputs_price
                input_item_price = int(percent_of_input_trade*trade_outputs_price)
                trades[input_item_price] = trade
            best_trade_value = max(trades.keys())
            return (best_trade_value, trades[best_trade_value])

    @cached_property
    def no_intel_sell_prices(self):
        '''
        Returns a dictionary of {sell_price: sell_source}
        '''
        max_item_trade_price_no_intel, max_item_trade_source_no_intel = self.max_input_trade_price_and_source_no_intel()
        sell_prices = {self.market_sell_price_no_intel: 'Market', max_item_trade_price_no_intel: max_item_trade_source_no_intel, self.highest_sell_price_to_trader: self.highest_sell_price_trader}
        return sell_prices

    @cached_property
    def intel_sell_prices(self):
        '''
        Returns a dictionary of {sell_price: sell_source}
        '''
        max_item_trade_price_intel, max_item_trade_source_intel = self.max_input_trade_price_and_source_intel()
        sell_prices = {self.market_sell_price_intel: 'Market', max_item_trade_price_intel: max_item_trade_source_intel, self.highest_sell_price_to_trader: self.highest_sell_price_trader}
        return sell_prices

    @cached_property
    def max_sell_price_no_intel(self):
        '''
        Returns the best sell price for this item, selected out of trades where this item is an input, traders, and the market.
        '''
        best_sell_price_no_intel = max([i for i in self.no_intel_sell_prices.keys() if i is not None])
        return best_sell_price_no_intel
    
    @cached_property
    def max_sell_price_intel(self):
        '''
        Returns the best sell price for this item, selected out of trades where this item is an input, traders, and the market.
        '''
        best_sell_price_intel = max([i for i in self.intel_sell_prices.keys() if i is not None])
        return best_sell_price_intel
    
    @cached_property
    def max_sell_price_no_intel_source(self):
        '''
        Returns the source of the best sell price for this item, selected out of trades where this item is an input, traders, and the market
        '''
        return self.no_intel_sell_prices[self.max_sell_price_no_intel]
    
    @cached_property
    def max_sell_price_no_intel_source_is_trade(self):
        '''
        Returns whether the source of the best sell price for this item is a trade
        '''
        if type(self.max_sell_price_no_intel_source) == str:
            return False
        return True

    @cached_property
    def max_sell_price_intel_source(self):
        '''
        Returns the source of the best sell price for this item, selected out of trades where this item is an input, traders, and the market
        '''
        return self.intel_sell_prices[self.max_sell_price_intel]

    @cached_property
    def max_sell_price_intel_source_is_trade(self):
        '''
        Returns whether the source of the best sell price for this item is a trade
        '''
        if type(self.max_sell_price_intel_source) == str:
            return False
        return True

    def __unicode__(self):
        """Returns a string representation of an item."""
        return self.name

    def __str__(self):
        return self.name

class Trade(models.Model):
    traders = ['', 'Prapor', 'Therapist', 'Fence', 'Skier',
               'Peacekeeper', 'Mechanic', 'Ragman', 'Jaeger']
    traders = [(i, i) for i in traders]
    trader_levels = [('', ''), ('I', 'I'), ('II', 'II'), ('III', 'III'), ('Max', 'Max')]
    trader = models.CharField(choices=traders, max_length=200, default=traders[0], blank=True)
    trader_level = models.CharField(choices=trader_levels, max_length=200, default=trader_levels[0], blank=True)
    crafting_stations = ['', 'Booze Generator', 'Intelligence Center', 'Lavatory', 'Medstation',
                         'Nutrition Unit', 'Water Collector', 'Workbench']
    crafting_stations = [(i, i) for i in crafting_stations]
    crafting_levels = trader_levels[:-1]
    crafting_station = models.CharField(choices=crafting_stations, max_length=200, default=crafting_stations[0], blank=True)
    crafting_station_level = models.CharField(choices=crafting_levels, max_length=200, default=crafting_levels[0], blank=True)
    input_items = models.ManyToManyField(Item, through='InputCount', related_name='inputs')
    output_items = models.ManyToManyField(Item, through='OutputCount', related_name='outputs')


    def clean(self):
        if (not self.trader or not self.trader_level) and (not self.crafting_station or not self.crafting_station_level): # Need one of these
            raise ValidationError({'trader': 'Should have either a trader and trader level or a crafting station and crafting station level'})
        elif (self.trader or self.trader_level) and (self.crafting_station or self.crafting_station_level): # Can't have both
            raise ValidationError({'trader': 'Should have either a trader or a crafting station, not both'})

    @cached_property
    def is_crafting(self):
        if not self.trader:
            return True
        return False

    @cached_property
    def inputs_buy_price_no_intel(self): # Minimum cost to buy/trade/craft all inputs
        return sum([i.amount * i.item.min_buy_price_no_intel for i in self.inputcount_set.all()])

    @cached_property
    def inputs_buy_price_intel(self): # Minimum cost to buy/trade/craft all inputs
        return sum([i.amount * i.item.min_buy_price_intel for i in self.inputcount_set.all()])

    @cached_property
    def outputs_price_no_intel(self): # Value of outputs with no intel center
        return sum([i.amount * i.item.max_sell_price_no_intel for i in self.outputcount_set.all()])

    @cached_property
    def outputs_price_intel(self): # Value of outputs with intel center
        return sum([i.amount * i.item.max_sell_price_intel for i in self.outputcount_set.all()])

    @cached_property
    def profit_no_intel(self): # Value of trade with no intel center
        return self.outputs_price_no_intel - self.inputs_buy_price_no_intel

    @cached_property
    def profit_intel(self): # Value of trade with no intel center
        return self.outputs_price_intel - self.inputs_buy_price_intel

    @cached_property
    def is_useless_no_intel(self): # Checks whether this trade is a negative value even with minimum value of inputs, and never worth it
        if self.profit_no_intel <= 0:
            return True
        else:
            return False
    
    @cached_property
    def is_useless_intel(self): # Checks whether this trade is a negative value even with minimum value of inputs, and never worth it
        if self.profit_intel <= 0:
            return True
        else:
            return False


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