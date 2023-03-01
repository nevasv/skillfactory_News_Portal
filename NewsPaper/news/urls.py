from django.urls import path
from .views import *

urlpatterns = [
    path('', news_page_list),
    path('authors/', AuthorsPage.as_view()),
    path('post/<int:pk>/', PostDetail.as_view()),
]
