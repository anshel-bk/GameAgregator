from game_info_part.models import GradesArticle, Article


def change_rating_func(user: str, article_slug: str, user_rating: str) -> None:
    """Функция изменения рейтинга статей"""
    grade_exists = GradesArticle.objects.filter(username=user, slug_article=article_slug)
    current_article = Article.objects.get(slug=article_slug)
    if not len(grade_exists):
        create_new_grade(current_article, user, article_slug, user_rating)
    else:
        change_grade(current_article, user, article_slug, user_rating)


def change_grade(current_article: Article, user: str, article_slug: str, user_rating: str) -> None:
    """Функция изменения при наличии текущей оценки"""
    current_grade = GradesArticle.objects.get(username=user, slug_article=article_slug)
    current_grade.grade = user_rating
    current_grade.save()
    grades = [obj.grade for obj in GradesArticle.objects.filter(slug_article=article_slug)]
    current_article.rating = round(sum(grades) / len(grades),2)
    current_article.save()


def create_new_grade(current_article: Article, user: str, article_slug: str, user_rating: str) -> None:
    """Функция изменения при создании новой оценки"""
    GradesArticle.objects.create(slug_article=article_slug, grade=user_rating, username=user)
    grades = [obj.grade for obj in GradesArticle.objects.filter(slug_article=article_slug)]
    current_article.rating = round(sum(grades) / len(grades),2)
    current_article.save()
