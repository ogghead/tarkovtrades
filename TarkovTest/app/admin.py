from django.contrib import admin

# Register your models here.

from app.models import Item, Trade, InputCount, OutputCount

admin.site.register(Item)
admin.site.register(Trade)
admin.site.register(InputCount)
admin.site.register(OutputCount)
