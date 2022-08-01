from django.db.models import QuerySet

from game_info_part.models import AuthorArticle, Article
from typing import Type, Union


def search_by_author_strict(value: str) -> Type[QuerySet] | None:
    res = AuthorArticle.objects.filter(author=value.strip())
    if len(res):
        ids = AuthorArticle.objects.filter(author=value.strip())[0].id
        result = Article.objects.filter(author=ids)
        return result


def search_by_article(value: str) -> Type[QuerySet] | None:
    result = Article.objects.filter(title__icontains=value)
    if result:
        return result


def search_by_all(search_value: str) -> Type[QuerySet] | bool:
    value = search_value
    result_author = search_by_author_strict(value)
    result_article = search_by_article(value)
    if result_author:
        return result_author
    elif result_article:
        return result_article
    else:
        return False
