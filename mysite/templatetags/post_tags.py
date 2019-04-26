from django import template
from ..models import Category

import markdown
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag('post/category.html')
def show_categorys():
    categories = Category.objects.all()
    return {'categories': categories}


# 文本编辑器
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text,
                                       extensions=['markdown.extensions.tables',
                                                   'markdown.extensions.fenced_code',
                                                   'markdown.extensions.codehilite', ]))
