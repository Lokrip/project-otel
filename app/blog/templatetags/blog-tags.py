from django import template
from django.utils.http import urlencode
from config.models import CatygoryBlog, TagsBlog, Blog

register = template.Library()


@register.simple_tag(name='get_cat')
def get_catygory():
    return CatygoryBlog.objects.all()

@register.simple_tag(name='get_tags')
def get_tags():
    return TagsBlog.objects.all()

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)

@register.inclusion_tag('blog/tags-includes/recent_post.html')
def get_recent_post():
    blogList = Blog.objects.order_by('-id')[:4]
    context = {'blogList': blogList}
    return context
