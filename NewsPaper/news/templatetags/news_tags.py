from django import template
from news.models import *

register = template.Library()


@register.simple_tag()
def get_posts():  # get_posts(name='gp')
    """" Это функция простого тега с декоратором simple_tag
    в шаблоне  есть {% load news_tags %} и далее {% get_posts as posts_list %},
    что позволяет в нужном месте проитерировать posts_list с выводом нужных значений на страницу
    """

    return Post.objects.all().order_by('-rating')[:2]


@register.simple_tag()
def get_latest_post():
    """ .latest() - это вывод последнего в итерации объекта по значению в ()"""

    return Post.objects.all().latest('dataCreations')


@register.inclusion_tag('news/tag.html')
def show_comments(sort="-rating", sort_param=0):
    """ Это функция включающего тега с декоратором inclusion_tag
      есть шаблон тегов в котором происходит работа с comments3, а затем
      в нужное место страницы вставляется это кусок кода {% show_comments %}
      Дополнительный параметр sort_param в этом случае доступен для работы в tag.html
      В основном шаблоне страницы уже сможем для изменения отображения
      использовать одноименный тег sort_param
      """
    if not sort:
        comments3 = Comment.objects.all()
    else:
        comments3 = Comment.objects.all().order_by(sort)[:2]

    return {'comments3': comments3, 'sort_param': sort_param}
