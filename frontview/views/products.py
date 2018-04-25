from django.shortcuts import render


def products(request):
    context = {'title': 'محصولات'}
    return render(request, 'frontview/products.html', context)
