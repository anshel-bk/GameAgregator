from django.test import TestCase

# Create your tests here.
from game_info_part.models import Article


class ArticleTests(TestCase):

    def test_check_published(self):
        check_pub = all([obj.is_published for obj in Article.objects.all()])
        self.assertIs(check_pub, True)
