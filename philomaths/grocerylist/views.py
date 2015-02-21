from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.forms import ModelForm

from grocerylist.models import List, Product, ProductOrder

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
    if request.POST.has_key('tag') and request.POST['tag'] != 'none':
        tag = request.POST['tag']
        form = AddListForm(request.POST)
        print 'using add to list'
    elif request.method == 'POST':
        tag = 'none'
        form = ListForm(request.POST)
    else:
        tag = 'none'
        form = ListForm()

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
                    order.save()
                    l.products.add(order)
                    l.save()
                except List.DoesNotExist:
                    print 'list does not exist'
    else:
            l = List(name='bob')
            l.save()
            tag = l.uuid
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
    template = loader.get_template('displayresult.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
