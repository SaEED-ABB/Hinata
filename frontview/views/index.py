from django.shortcuts import render


def index(request):
    context = {'title': 'خانه'}
    template = "index.html"
    return render(request, template, context)
