from django.contrib import admin
from django.forms import ModelForm
from django.db.models import F, ExpressionWrapper, IntegerField
# Register your models here.

from app.models import Item, Trade, InputCount, OutputCount

class InputInlineAdmin(admin.TabularInline):
    model = Trade.input_items.through

class OutputInlineAdmin(admin.TabularInline):
    model = Trade.output_items.through

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 
                    'min_buy_price_no_intel', 'min_buy_price_no_intel_source',
                    'min_buy_price_intel', 'min_buy_price_intel_source',
                    'max_sell_price_no_intel', 'max_sell_price_no_intel_source',
                    'max_sell_price_intel', 'max_sell_price_intel_source')
    def add_view(self, request, extra_content=None):
        self.fieldsets = [
            (None, {'fields': ['name']}),
            ('True Value', {'fields': ['true_value'], 'description': '''True value is calculated as follows:
                                                                        1) Record the value of your stash as X.
                                                                        2) Sell the item to a trader, record the value of rubles you get as Y.
                                                                        3) Record the value of your stash after selling the item as Z.
                                                                        4) Calculate X + Y - Z, the result is the true value.'''}),
            ('Trader Data', {'fields': [['highest_sell_price_to_trader', 'highest_sell_price_trader'], 
                                        ['lowest_buy_price_from_trader', 'lowest_buy_price_trader']]}),
            ('Market Data', {'fields': ['market_buy_price']}),
        ]
        return super(ItemAdmin,self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        self.fieldsets = [
            (None, {'fields': ['name']}),
            ('True Value', {'fields': ['true_value'], 'description': '''True value is calculated as follows:
                                                                        1) Record the value of your stash as X.
                                                                        2) Sell the item to a trader, record the value of rubles you get as Y.
                                                                        3) Record the value of your stash after selling the item as Z.
                                                                        4) Calculate X + Y - Z, the result is the true value.'''}),
            ('Trader Data', {'fields': [['highest_sell_price_to_trader', 'highest_sell_price_trader'], 
                                        ['lowest_buy_price_from_trader', 'lowest_buy_price_trader']]}),
            ('Market Data', {'fields': ['market_buy_price']}),
            ('Market Data (Read Only)', {'fields': [['fee_to_post_at_buy_price_no_intel', 'market_sell_price_no_intel'],
                                                    ['fee_to_post_at_buy_price_intel', 'market_sell_price_intel']]}),
            ('Calculated Fields (Read Only)', {'fields': [['min_buy_price_no_intel', 'min_buy_price_no_intel_source', 'min_buy_price_no_intel_source_is_trade'],
                                                          ['min_buy_price_intel', 'min_buy_price_intel_source', 'min_buy_price_intel_source_is_trade'],
                                                          ['max_sell_price_no_intel', 'max_sell_price_no_intel_source', 'max_sell_price_no_intel_source_is_trade'],
                                                          ['max_sell_price_intel', 'max_sell_price_intel_source', 'max_sell_price_intel_source_is_trade']]}),
        ]
        self.readonly_fields = ('fee_to_post_at_buy_price_no_intel', 'market_sell_price_no_intel',
                                'fee_to_post_at_buy_price_intel', 'market_sell_price_intel',
                                'min_buy_price_no_intel', 'min_buy_price_no_intel_source', 'min_buy_price_no_intel_source_is_trade',
                                'min_buy_price_intel', 'min_buy_price_intel_source', 'min_buy_price_intel_source_is_trade',
                                'max_sell_price_no_intel', 'max_sell_price_no_intel_source', 'max_sell_price_no_intel_source_is_trade',
                                'max_sell_price_intel', 'max_sell_price_intel_source', 'max_sell_price_intel_source_is_trade')
        return super(ItemAdmin,self).change_view(request, object_id)


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('trader', 'trader_level', 
                    'profit_no_intel', 'profit_intel', 
                    'is_useless_no_intel', 'is_useless_intel')

    inlines = (InputInlineAdmin, OutputInlineAdmin,)
    def add_view(self, request, extra_content=None):
        self.fieldsets = [
            (None, {'fields': ['trader', 'trader_level']}),
        ]
        return super(TradeAdmin,self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        self.fieldsets = [
            (None, {'fields': ['trader', 'trader_level']}),
            ('Calculated Fields (Read Only)', {'fields': [['inputs_buy_price_no_intel', 'inputs_buy_price_intel'],
                                                          #['min_inputs_price_intel', 'max_inputs_price_intel'],
                                                          ['outputs_price_no_intel', 'outputs_price_intel'],
                                                          #['min_profit_no_intel', 'max_profit_no_intel'],
                                                          #['min_profit_intel','max_profit_intel'],
                                                          ['profit_no_intel', 'profit_intel'],
                                                          ['is_useless_no_intel','is_useless_intel']]})
        ]
        self.readonly_fields = ('inputs_buy_price_no_intel', 'inputs_buy_price_intel', 
                                #'min_inputs_price_intel', 'max_inputs_price_intel',
                                'outputs_price_no_intel', 'outputs_price_intel',
                                #'min_profit_no_intel', 'max_profit_no_intel',
                                #'min_profit_intel','max_profit_intel',
                                'profit_no_intel', 'profit_intel',
                                'is_useless_no_intel','is_useless_intel')
        return super(TradeAdmin,self).change_view(request, object_id)


