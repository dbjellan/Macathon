from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.forms import ModelForm

from decimal import Decimal

from grocerylist.models import List, Product, ProductOrder, Store, StoreProduct

class ListForm(forms.Form):
    name = forms.CharField()
    products = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity = forms.IntegerField()

class AddListForm(forms.Form):
    products = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity = forms.IntegerField()

class TestForm(ModelForm):
    class Meta:
            model = List

class ProductForm(ModelForm):
    class Meta:
        model = Product


def createlist(request):
    if request.method == 'POST' and request.POST['action'] == 'Find Store':
        return displayresult(request)

    if request.method == 'POST' and not request.POST.has_key('name'):
        form = AddListForm(request.POST)
        print 'using add to list'
    elif request.method == 'POST':
        form = ListForm(request.POST)
    else:
        form = ListForm()


    if request.POST.has_key('tag') and request.POST['tag'] != 'none':
        tag = request.POST['tag']
    else:
        tag = 'none'

    if request.method == 'POST':
        if form.is_valid():
            product = form.cleaned_data['products']
            quantity = form.cleaned_data['quantity']
            if tag == 'none':
                order = ProductOrder(product=product, quantity=quantity)
                order.save()
                l = List(name=form.cleaned_data['name'])
                l.save()
                l.products.add(order)
                tag = l.uuid
                print 'saving tag' + tag
                l.save()
            else:
                try:
                    l = List.objects.get(uuid=tag)
                    order = ProductOrder(product=product, quantity=quantity)
                    if request.POST.has_key('name'):
                        l.name = form.cleaned_data['name']
                    order.save()
                    l.products.add(order)
                    l.save()
                except List.DoesNotExist:
                    print 'list does not exist'
    else:
        l = List(name='My List')
        l.save()
        tag = l.uuid

    if request.POST.has_key('name'):
        form = AddListForm()

    try:    
        l = List.objects.get(uuid=tag)
        item_list = l.products
        name = List.objects.get(uuid=tag).name
    except List.DoesNotExist:
        item_list = []
        name = "New List"

    template = loader.get_template('createlist.html')

    context = RequestContext(request, {
        'item_list' : item_list,
        'form' : form.as_table(),
        'tag' : tag,
        'name' : name

    })

    return HttpResponse(template.render(context))

def displayresult(request):
    if request.POST.has_key('tag'):
        tag = request.POST['tag']
        l = List.objects.get(uuid=tag)
        min_price = Decimal(1000000)
        price = 0.0
        best_store = ''
        for store in Store.objects.all():
            price = Decimal(0.0)
            for item in l.products.all():
                storeproduct = StoreProduct.objects.get(store=store, product=item.product)
                price += storeproduct.price * item.quantity
            if price < min_price:
                min_price = price
                best_store = store.name

    name = l.name
    template = loader.get_template('displayresult.html')
    context = RequestContext(request, {
        'item_list' : l.products.all(),
        'tag' : tag,
        'name' : name,
        'store' : best_store,
        'price' : min_price,
    })
    return HttpResponse(template.render(context))

def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def inputimage(request):
    template = loader.get_template('inputimage.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def contact(request):
    template = loader.get_template('contact.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def about(request):
    template = loader.get_template('about.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
