from django.shortcuts import get_list_or_404, render
from django.core.paginator import Paginator
from goods.models import Products

def catalog(request, company_slug, page = 1):
    if company_slug == 'all':
        goods = Products.objects.all()
    else:
        goods = get_list_or_404(Products.objects.filter(company__slug = company_slug))
            
    paginator = Paginator(goods, 6)
    current_page = paginator.page(page)
    context = {
        'title': 'BJGeDrenouille - Каталог',
        'goods': current_page,
        "slug_url": company_slug
    }
    return render(request, 'goods/catalog.html', context)

def product(request, product_slug):

    product = Products.objects.get(slug = product_slug)

    context = {
        'product': product
    }

    return render(request, 'goods/product.html', context=context)