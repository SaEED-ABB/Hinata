from django.shortcuts import render

from store.models import Category


def index(request):
    context = {'title': 'خانه', 'categories': Category.objects.all(), }
    return render(request, 'frontview/index.html', context)
