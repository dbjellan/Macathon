from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.forms import ModelForm

from grocerylist.models import List, Product

class ListForm(forms.Form):
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all())

class TestForm(ModelForm):
    class Meta:
            model = List

class ProductForm(ModelForm):
    class Meta:
        model = Product


def createlist(request):
    if request.method == 'POST':
        pass
    
    item_list = ['boob', 'penis']
    template = loader.get_template('createlist.html')
    form = ListForm()

    context = RequestContext(request, {
        'item_list' : item_list,
        'form' : form.as_table(),
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
