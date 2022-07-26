from django.shortcuts import render

# Create your views here.
from .models import Article
from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = "game_info_part/home.html"

    def get_context_data(self, **kwargs):
        articles = Article.objects.all()
        context = {"title": "Главная страница","articles":articles}
        return context
