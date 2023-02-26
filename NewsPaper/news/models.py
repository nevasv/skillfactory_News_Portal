from django.db import models
from django.contrib.auth.models import User
from param import *
from django.db.models import Sum


class Author(models.Model):
    """
    Модель Author
    имеет следующие поля:
    -<portalUser> связь «один к одному» с встроенной моделью пользователей User;
    - <ratingAuthor> рейтинг пользователя.
    """
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        """
        - update_rating() модели Author, который обновляет рейтинг пользователя, переданный в аргумент этого метода.
        Он состоит из следующего:
        -суммарный рейтинг каждой статьи автора умножается на 3;
        -суммарный рейтинг всех комментариев автора;
        -суммарный рейтинг всех комментариев к статьям автора.
        """

        postR = self.post_set.all().aggregate(postRating=Sum('rating'))
        p_R = 0
        p_R += postR.get('postRating')

        commentR = self.authorUser.comment_set.all().aggregate(commentRating=Sum('rating'))
        c_R = 0
        c_R += commentR.get('commentRating')

        self.ratingAuthor = p_R * 3 + c_R
        self.save()

    def __str__(self):
        return f"{self.authorUser}"


class Category(models.Model):
    """
    Модель Category
    Темы, которые они отражают (спорт, политика, образование и т. д.).
    Имеет единственное поле: название категории.
    - <name> Поле должно быть уникальным (в определении поля необходимо написать параметр unique = True).
    """
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name}"


class Post(models.Model):
    """
    Модель Post
    Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
    Каждый объект может иметь одну или несколько категорий.
    Соответственно, модель должна включать следующие поля:
    - <author>        связь «один ко многим» с моделью Author;
    - <categoryFild>  поле с выбором — «статья» или «новость»;
    - <dataCreations> автоматически добавляемая дата и время создания;
    - <postCategory>  связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    - <title>         заголовок статьи/новости;
    - <text>          текст статьи/новости;
    - <rating>        рейтинг статьи/новости.
    """
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categoryType = models.CharField(max_length=20, choices=CATEGORY_CHOISES, default=ARTICLE)
    dataCreations = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        """
        - like()    который увеличивает рейтинг на единицу.
        """
        self.rating += 1
        self.save()

    def dislike(self):
        """
        - dislike() который уменьшают рейтинг на единицу.
        """
        self.rating -= 1
        self.save()

    def preview(self):
        """
        - preview() модели Post, который возвращает начало статьи
        (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце.
        """
        return self.text[0:128] + '...'

    def __str__(self):
        dataf = 'Post from {}'.format(self.dataCreations.strftime('%d.%m.%Y %H:%M'))
        return f"{dataf},{self.author},{self.title}"


class PostCategory(models.Model):
    """
    Модель PostCategory
    Промежуточная модель для связи «многие ко многим»:
    - <postThrough>     связь «один ко многим» с моделью Post;
    - <categoryThrough> связь «один ко многим» с моделью Category.
    """
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.postThrough},from the category:  {self.categoryThrough}"


class Comment(models.Model):
    """
    Модель Comment
    Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
    Модель будет иметь следующие поля:
    - <commentPost>  связь «один ко многим» с моделью Post;
    - <userPost>     связь «один ко многим» со встроенной моделью User
                    (комментарии может оставить любой пользователь, необязательно автор);
    - <text>         текст комментария;
    - <dataCreation> дата и время создания комментария;
    - <rating>       рейтинг комментария.
    """
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    userPost = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dataCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        """
        - like()    который увеличивает рейтинг на единицу.
        """
        self.rating += 1
        self.save()

    def dislike(self):
        """
        - dislike() который уменьшают рейтинг на единицу.
        """
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"{self.dataCreation}, {self.userPost}"
