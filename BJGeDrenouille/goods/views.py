from django.shortcuts import get_list_or_404, render
from django.core.paginator import Paginator
from goods.utils import q_search
from goods.models import Products

def catalog(request, company_slug=None):
    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)


    if company_slug == 'all':
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = get_list_or_404(Products.objects.filter(company__slug = company_slug))

    if on_sale:
        goods = goods.filter(discount__gt=0)   
    if order_by and order_by != 'default':
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 6)
    current_page = paginator.page(int(page))
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