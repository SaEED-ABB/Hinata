from django.shortcuts import render, get_object_or_404

from store.models import Category, ProductFilter, Product, ProductImage


def products(request):
    context = {
        'title': 'محصولات',
        'categories': Category.objects.all(),
        'filters': ProductFilter.get_all_info()
    }
    return render(request, 'store/products.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product.view_counter += 1
    product.save()

    # views_counter = request.session.get(product.slug, 0)
    # request.session[product.slug] = views_counter + 1

    return render(request, 'store/dress.html')


def product_image_detail(request, product_slug, image_slug):
    product = get_object_or_404(Product, slug=product_slug)
    image = get_object_or_404(product.images, slug=image_slug)

    return render(request, 'frontview/fullImage.html', {'image': image})
