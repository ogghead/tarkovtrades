"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from app.models import Item, Trade

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Tarkov Trader',
            'year':datetime.now().year,
            'has_intel': False,
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
