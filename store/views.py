from django.shortcuts import render

from store.models import Category, ProductFilter


def products(request):
    context = {
        'title': 'محصولات',
        'categories': Category.objects.all(),
        'filters': ProductFilter.get_all_info()
    }
    return render(request, 'store/products.html', context)
