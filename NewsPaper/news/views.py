from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
# from django.views.generic.edit import FormView
from .models import *


class AuthorsPage(ListView):
    model = Author  # queryset = Author.objects.all()
    context_object_name = "Authors"
    template_name = 'news/authors.html'


class Post(DetailView):
    model = Post
    context_object_name = 'Posts'
    template_name = 'news/posts.html'


def news_page_list(request):
    """ Представление для вывода страницы с новостями по заданию D3.6 """
   # newslist = Post.objects.all().order_by('-rating')[:6]  {'newslist': newslist}

    return render(request, 'news/news.html')


# class Myform(FormView):
#     form_class = myform
#     success_url = "/succsess/"
#
#     def form_valid(self, form):
#         return super().form_valid(form)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
