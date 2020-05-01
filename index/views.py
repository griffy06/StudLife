from django.shortcuts import render


def index(request):

    return render(request, 'index/index_page.html')


def about(request):
    return render(request, 'index/about_page.html')


def developers(request):
    return render(request, 'index/developers_page.html')


def loading(request):
    return render(request, 'index/loading_page.html')