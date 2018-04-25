from django.shortcuts import render


def products(request):
    context = {'title': 'محصولات'}
    template = "products.html"
    return render(request, template, context)
