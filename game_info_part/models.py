from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Article(models.Model):
    author = models.ForeignKey(
        'AuthorArticle',
        null=True, on_delete=models.SET_NULL,
        verbose_name="Автор статьи", )

    name_game = models.CharField(
        blank=False,
        verbose_name="Название игры",
        max_length=255)

    title = models.CharField(
        max_length=500,
        verbose_name="Заголовок статьи")

    is_published = models.BooleanField(
        verbose_name="Факт публикации",
        blank=False)

    contains = models.TextField(
        blank=False,
        verbose_name="Содержимое статьи")

    preview_picture = models.ImageField(
        upload_to="photos/%Y/%m/%d/",
        verbose_name="Превью картинка",
        blank=True)

    date_published = models.DateField(
        verbose_name="Дата публикации",
        auto_now_add=True)

    rating = models.FloatField(
        verbose_name="Рейтинг",
        blank=True,
        null=0)

    slug = models.SlugField(
        verbose_name="Слаг",
        max_length=255)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'article_slug': self.slug})


class AuthorArticle(models.Model):
    author = models.CharField(
        max_length=100,
        db_index=True)

    def __str__(self):
        return self.author


class GradesArticle(models.Model):

    slug_article = models.SlugField(
        verbose_name="Слаг",
        max_length=255)

    grade = models.IntegerField(
        verbose_name="Оценка"
    )

    username = models.CharField(
        verbose_name="Никнейм пользователя",
        max_length=255)


class Comment(models.Model):
    post = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.text