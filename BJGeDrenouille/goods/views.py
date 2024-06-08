from django.shortcuts import get_list_or_404, render

from goods.models import Products

def catalog(request, company_slug):
    if company_slug == 'all':
        goods = Products.objects.all()
    else:
        goods = get_list_or_404(Products.objects.filter(company__slug = company_slug))
            
    context = {
        'title': 'BJGeDrenouille - Каталог',
        'goods': goods
    }
    return render(request, 'goods/catalog.html', context)

def product(request, product_slug):

    product = Products.objects.get(slug = product_slug)

    context = {
        'product': product
    }

    return render(request, 'goods/product.html', context=context)