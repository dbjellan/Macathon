from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.forms import ModelForm

from grocerylist.models import List, Product

class ListForm(forms.Form):
    name = forms.CharField()
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all())

class TestForm(ModelForm):
    class Meta:
            model = List

class ProductForm(ModelForm):
    class Meta:
        model = Product


def createlist(request):
    if request.POST.has_key('tag'):
        tag = request.POST['tag']
    else:
        tag = 'none'
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['products']
            if tag == 'none':
                l = List(name=form.cleaned_data['name'])
                l.save()
                l.products.add(*product)
                tag = l.uuid
                l.save()
            else:
                try:
                    l = List.objects.get(uuid=tag)
                    l.products.add(*product)
                    l.save()
                except List.DoesNotExist:
                    pass
    try:    
        item_list = List.objects.get(uuid=tag).products
        name = List.objects.get(uuid=tag).name
    except List.DoesNotExist:
        item_list = []
        name = "New List"

    template = loader.get_template('createlist.html')
    form = ListForm()

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
