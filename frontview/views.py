from django.shortcuts import render

from store.models import Category, ProductFilter


def index(request):
    context = {'title': 'خانه', 'categories': Category.objects.all(), }

    ProductFilter.instantiate_yourself()  # this make "sort_by" filter and its options

    return render(request, 'frontview/index.html', context)
