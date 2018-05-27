from django.shortcuts import render, get_object_or_404

from store.models import Category, Product, ProductFilter, FilterOption


def index(request):
    context = {'title': 'خانه', 'categories': Category.objects.all(), }

    ProductFilter.instantiate_yourself()  # this make "sort_by" filter and its options

    return render(request, 'frontview/index.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product.view_counter += 1
    product.save()

    # views_counter = request.session.get(product.slug, 0)
    # request.session[product.slug] = views_counter + 1

    return render(request, 'store/dress.html')
