from django.shortcuts import render


def index(request):
    context = {'title': 'خانه'}
    return render(request, 'frontview/index.html', context)
