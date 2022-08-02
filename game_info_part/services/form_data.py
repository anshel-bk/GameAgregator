from django.core.handlers.wsgi import WSGIRequest

from game_info_part.models import AuthorArticle
from typing import Type


def adding_necessary_data(data: dict, request: Type[WSGIRequest]) -> dict:
    data['rating'] = 0
    nickname = request.user.username
    if not AuthorArticle.objects.filter(author=nickname):
        AuthorArticle.objects.create(author=nickname)
    data['author'] = AuthorArticle.objects.get(author=nickname)
    data['slug'] = slugify(data['title'])
    return data


def slugify(text: str) -> str:
    slug_dict = {
        'а': 'a', 'к': 'k', 'х': 'h', 'б': 'b', 'л': 'l', 'ц': 'c', 'в': 'v', 'м': 'm', 'ч': 'ch',
        'г': 'g', 'н': 'n', 'ш': 'sh', 'д': 'd', 'о': 'o', 'щ': 'shh', 'е': 'e', 'п': 'p', 'ъ': '',
        'ё': 'jo', 'р': 'r', 'ы': 'y', 'ж': 'zh', 'с': 's', 'ь': "", 'з': 'z', 'т': 't', 'э': 'je',
        'и': 'i', 'у': 'u', 'ю': 'ju', 'й': 'j', 'ф': 'f', 'я': 'ya'
    }
    text = ''.join([letter for letter in text if letter.isalpha() or letter.isspace()])
    text = text.replace(' ', '-')
    text = text.lower()
    result = ''
    for letter in text:
        result += slug_dict.get(letter, letter)
    return result
