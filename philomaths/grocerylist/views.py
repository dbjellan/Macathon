from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.forms import ModelForm

from grocerylist.models import List, Product

class ListForm(forms.Form):
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all())
    tag = forms.IntegerField(widget=forms.HiddenInput())

class TestForm(ModelForm):
    class Meta:
            model = List

class ProductForm(ModelForm):
    class Meta:
        model = Product


def createlist(request):
    tag = 'none'
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['products']
            if form.cleaned_data['tag'] == 'none':
                l = List(name=form.cleaned_data['name'])
                l.save()
                l.products.add(product)
                tag = l.uuid
                l.save()
    try:    
        item_list = List.objects.get(uuid=tag).products
    except List.DoesNotExist:
        item_list = []

    template = loader.get_template('createlist.html')
    form = ListForm()

    context = RequestContext(request, {
        'item_list' : item_list,
        'form' : form.as_table(),
        'tag' : tag
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
