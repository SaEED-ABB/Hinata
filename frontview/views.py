from django.shortcuts import render, get_object_or_404

from store.models import Category, Product


def index(request):
    context = {'title': 'خانه', 'categories': Category.objects.all(), }
    return render(request, 'frontview/index.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/dress.html')