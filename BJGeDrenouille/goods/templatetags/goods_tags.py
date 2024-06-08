from django import template
from goods.models import Companies


register = template.Library()


@register.simple_tag()
def tag_companies():
    return Companies.objects.all()