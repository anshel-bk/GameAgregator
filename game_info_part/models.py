from django.db import models
from django.urls import reverse


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
