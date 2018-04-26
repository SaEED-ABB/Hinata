from django.shortcuts import render

from store.models import Category


def products(request):
    context = {'title': 'محصولات', 'categories': Category.objects.all()}
    return render(request, 'store/products.html', context)
