from django.contrib import admin
from django.forms import ModelForm
# Register your models here.

from app.models import Item, Trade, InputCount, OutputCount

class InputInlineAdmin(admin.TabularInline):
    model = Trade.input_items.through

class OutputInlineAdmin(admin.TabularInline):
    model = Trade.output_items.through

class ItemAddForm(ModelForm):
    model = Item
    fields = ('name', ('highest_sell_price_to_trader', 'highest_sell_price_trader'), 
              ('lowest_buy_price_from_trader', 'lowest_buy_price_trader'), 
              'market_buy_price')

class ItemChangeForm(ModelForm):
    model = Item
    fields = ('name', ('highest_sell_price_to_trader', 'highest_sell_price_trader'), 
              ('lowest_buy_price_from_trader', 'lowest_buy_price_trader'),
              'market_buy_price', 'market_sell_price_no_intel',
              'market_sell_price_intel', 'min_buy_price',
              'max_sell_price_no_intel', 'max_sell_price_intel')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fields = ('name', ('highest_sell_price_to_trader', 'highest_sell_price_trader'), 
              ('lowest_buy_price_from_trader', 'lowest_buy_price_trader'),
              'market_buy_price', 'market_sell_price_no_intel',
              'market_sell_price_intel', 'min_buy_price',
              'max_sell_price_no_intel', 'max_sell_price_intel')
    readonly_fields = ('market_sell_price_no_intel', 'market_sell_price_intel', 'min_buy_price',
                       'max_sell_price_no_intel', 'max_sell_price_intel')

    def add_view(self, request, extra_content=None):
         self.fields = ('name', ('highest_sell_price_to_trader', 'highest_sell_price_trader'), 
                        ('lowest_buy_price_from_trader', 'lowest_buy_price_trader'), 
                        'market_buy_price')
         self.readonly_fields = ()
         return super(ItemAdmin,self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
         self.fields = ('name', ('highest_sell_price_to_trader', 'highest_sell_price_trader'), 
                        ('lowest_buy_price_from_trader', 'lowest_buy_price_trader'),
                        'market_buy_price', 'market_sell_price_no_intel',
                        'market_sell_price_intel', 'min_buy_price',
                        'max_sell_price_no_intel', 'max_sell_price_intel')
         self.readonly_fields = ('market_sell_price_no_intel', 'market_sell_price_intel', 'min_buy_price',
                                 'max_sell_price_no_intel', 'max_sell_price_intel')
         return super(ItemAdmin,self).change_view(request, object_id)

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    fields = ('trader',)
    inlines = (InputInlineAdmin, OutputInlineAdmin,)
