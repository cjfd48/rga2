from django import template
from presupuestacion.models import Proyecto

register = template.Library()

@register.inclusion_tag('presupuestacion/cats.html')
def get_category_list(cat=None):
    print(cat)
    return {'cats': Proyecto.objects.all(), 'act_cat': cat}
