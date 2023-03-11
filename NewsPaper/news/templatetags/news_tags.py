from django import template
from news.models import *

register = template.Library()


@register.simple_tag()
def get_posts():  # get_posts(name='gp')

    return Post.objects.all().order_by('-rating')[:2]


@register.inclusion_tag('news/tag.html')
def show_comments():

    comments3 = Comment.objects.all().order_by('-rating')[:2]

    return {'comments3': comments3}
