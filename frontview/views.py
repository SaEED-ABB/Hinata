from django.shortcuts import render, get_object_or_404

from store.models import Category, Product, ProductFilter, FilterOption


def index(request):
    context = {'title': 'خانه', 'categories': Category.objects.all(), }
    sort_filter = ProductFilter.objects.get_or_create(name='مرتب سازی بر اساس', slug='sort-by')[0]
    sort_filter.options.get_or_create(name='جدید ترین', slug='newest')
    sort_filter.options.get_or_create(name='پر بازدید ترین', slug='most-viewed')
    sort_filter.options.get_or_create(name='محبوب ترین', slug='most-favorite')

    return render(request, 'frontview/index.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/dress.html')
