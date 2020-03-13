from django.contrib import admin

# Register your models here.

from app.models import Item, Trade, InputCount, OutputCount

class InputInlineAdmin(admin.TabularInline):
    model = Trade.input_items.through

class OutputInlineAdmin(admin.TabularInline):
    model = Trade.output_items.through

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['trader']})
    ]

    inlines = (InputInlineAdmin, OutputInlineAdmin,)

admin.site.register(InputCount)
admin.site.register(OutputCount)
