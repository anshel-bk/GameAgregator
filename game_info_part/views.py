from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = "game_info_part/home.html"

    def get_context_data(self, **kwargs):
        context = {"title": "Главная страница"}
        return context
