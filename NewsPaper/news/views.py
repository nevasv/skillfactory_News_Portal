from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import ListView, DetailView
# from django.views.generic.edit import FormView
from  django.views.generic.base import View
from .models import *

bad_names = ['incidents', 'Дурак', 'Гад']


class AuthorsPage(ListView):
    model = Author  # queryset = Author.objects.all()
    context_object_name = "Authors"
    template_name = 'news/authors.html'


class PostDetail(View):
    def get(self, request, pk):
        ps = Post.objects.get(id=pk)
        return render(request, "news/posts.html", {'ps':ps})


def news_page_list(request):
    """ Представление для вывода страницы с новостями по заданию D3.6 """

    newslist = Post.objects.all().order_by('-rating')[:6]

    return render(request, 'news/news.html', {'newslist': newslist})


# class Myform(FormView):
#     form_class = myform
#     success_url = "/succsess/"
#
#     def form_valid(self, form):
#         return super().form_valid(form)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
