"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.forms.formsets import formset_factory
from django.db.models import Q
from django.http import HttpRequest, HttpResponseRedirect
from app.models import Item, Trade
# from app.forms import ItemForm

def home(request):
    """Renders the home page."""
    ItemSet = formset_factory(ItemForm, extra=2) # Generate a formset for the item form
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        formset = ItemSet(request.POST)
        if formset.is_valid():
            items = {}
            for form in formset:
                items[form.cleaned_data.get('item')] = {'amount': form.cleaned_data.get('item_amount')}
            find_best_deals(items, False)
            return HttpResponseRedirect('/redirected/')

    formset = ItemSet()
    return render(
        request,
        'app/index.html',
        {
            'title':'Tarkov Trader',
            'year':datetime.now().year,
            'has_intel': False,
            'formset': formset,
        }
    )

def trades(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/trades.html',
        {
            'title':'Tarkov Trader',
            'year':datetime.now().year,
            'has_intel': False,
            'tradelist': Trade.objects.order_by('id'),
        }
    )

def trade(request, id):
    assert isinstance(request, HttpRequest)
    trade = get_object_or_404(Trade, id=id)
    return render(
        request,
        'app/trade.html',
        {
            'title':'Tarkov Trader',
            'year':datetime.now().year,
            'has_intel': False,
            'trade': trade,
        }
    )

def items(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/items.html',
        {
            'title':'Tarkov Trader',
            'year':datetime.now().year,
            'has_intel': False,
            'itemlist': Item.objects.order_by('name'),
        }
    )

def item(request, name):
    assert isinstance(request, HttpRequest)
    item = get_object_or_404(Item, name=name)
    return render(
        request,
        'app/item.html',
        {
            'title':'Tarkov Trader',
            'year':datetime.now().year,
            'has_intel': False,
            'item': item,
        }
    )

# def itempicker(request):
#     assert isinstance(request, HttpRequest)
#     if request.method == 'POST':
#         form = ItemPickerForm(request.POST)
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/redirected/')
#     else:
#         form = ItemPickerForm
#         return render(
#             request,
#             'app/itempicker.html',
#             {   'form': form,
#                 'title':'Tarkov Trader',
#                 'year':datetime.now().year,
#                 'has_intel': False,
#             }
#         )

# def recommendations(request, names):
#     assert isinstance(request, HttpRequest)
#     if request.method == 'POST':
#         form = ItemPickerForm(request.POST)
#         if form.is_valid():
#             items = form.cleaned_data.get('selected_items')
#     else:
#         form = ItemPickerForm

#     return render_to_response('render_country.html', {'form': form},
#                               context_instance=RequestContext(request))
    #item = get_object_or_404(Item, name=name)
    #return render(
    #    request,
    #    'app/item.html',
    #    {
    #        'title':'Tarkov Trader',
    #        'year':datetime.now().year,
    #        'has_intel': False,
    #        'item': item,
    #    }
    #)

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'year':datetime.now().year,
            'has_intel': False,
            'message':'Your contact page.',
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
