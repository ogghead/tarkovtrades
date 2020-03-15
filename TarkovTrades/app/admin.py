from django.contrib import admin
from django.forms import ModelForm
# Register your models here.

from app.models import Item, Trade, InputCount, OutputCount

class InputInlineAdmin(admin.TabularInline):
    model = Trade.input_items.through

class OutputInlineAdmin(admin.TabularInline):
    model = Trade.output_items.through

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    def add_view(self, request, extra_content=None):
         self.fields = ('name', 'true_value',
                        ('highest_sell_price_to_trader', 'highest_sell_price_trader'), 
                        ('lowest_buy_price_from_trader', 'lowest_buy_price_trader'), 
                        'market_buy_price',)
         return super(ItemAdmin,self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
         self.fields = ('name', 'true_value',
                        ('highest_sell_price_to_trader', 'highest_sell_price_trader'), 
                        ('lowest_buy_price_from_trader', 'lowest_buy_price_trader'),
                        'market_buy_price', 
                        ('fee_to_post_at_buy_price_no_intel', 'fee_to_post_at_buy_price_intel'), 
                        'market_sell_price_no_intel', 'market_sell_price_intel', ('min_buy_price', 'min_buy_price_source'),
                        ('max_sell_price_no_intel', 'max_sell_price_no_intel_source'), ('max_sell_price_intel', 'max_sell_price_intel_source'))
         self.readonly_fields = ('fee_to_post_at_buy_price_no_intel', 'fee_to_post_at_buy_price_intel',
                                 'market_sell_price_no_intel', 'market_sell_price_intel', 'min_buy_price', 'min_buy_price_source',
                                 'max_sell_price_no_intel', 'max_sell_price_no_intel_source', 'max_sell_price_intel', 'max_sell_price_intel_source')
         return super(ItemAdmin,self).change_view(request, object_id)


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    def add_view(self, request, extra_content=None):
         self.fields = ('trader', 'trader_level')
         return super(TradeAdmin,self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
         self.fields =  ('trader', 'trader_level', 
                         'inputs_sell_price_no_intel', 'inputs_sell_price_intel',
                         'outputs_sell_price_no_intel', 'outputs_sell_price_intel',
                         'net_value_no_intel', 'net_value_intel')
         self.readonly_fields = ('inputs_sell_price_no_intel', 'inputs_sell_price_intel',
                                 'outputs_sell_price_no_intel', 'outputs_sell_price_intel',
                                 'net_value_no_intel', 'net_value_intel')
         return super(TradeAdmin,self).change_view(request, object_id)
    inlines = (InputInlineAdmin, OutputInlineAdmin,)

