from django.http import HttpResponse
from django.shortcuts import render
 
from goods.models import Companies
def index(request):

    companies = Companies.objects.all()

    context = {
        'title': 'Home - Главная',
        'content': 'Магазин Сырков BJGeDrenouille',
        'companies': companies
    }
    return render(request, 'main/index.html', context)

 
def about(request):
    context = {
        'title': 'BJGeDrenouille - О нас',
        'content': 'О нас',
        'text_on_page': 'qweqweqweqweqweqweq we qw e qwe q we qwe '
    }
    return render(request, 'main/about.html', context)