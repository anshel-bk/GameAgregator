from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import RegisterUserForm, LoginUserForm, AddArticleForm
from .models import Article, AuthorArticle
from django.views.generic import TemplateView, CreateView, ListView

from .services.form_data import slugify, adding_necessary_data


class HomePage(ListView):
    template_name = "game_info_part/home.html"
    paginate_by = 6
    model = Article

    def get_context_data(self, **kwargs):
        articles = Article.objects.filter(is_published=True)
        paginator = Paginator(articles, 6)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {"title": "Главная страница",
                   'page_obj': page_obj}
        return context


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'game_info_part/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {"form": RegisterUserForm, 'title': 'Регистрация'}
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'game_info_part/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {"form": LoginUserForm, "title": 'Вход'}
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


class ShowArticle(TemplateView):
    template_name = 'game_info_part/show_article.html'

    def get_context_data(self, *, object_list=None, article_slug=None, **kwargs):
        data = Article.objects.get(slug=article_slug)
        context = {"data": data, "title": data.title}
        return context


def add_article(request):
    if request.method == 'POST':
        form = AddArticleForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                data = adding_necessary_data(form.cleaned_data, request)
                Article.objects.create(**data)
                return redirect('home')
            except Exception as ex:
                form.add_error(None, f"Ошибка добавления статьи.возникло исключение {ex}")
    else:
        form = AddArticleForm()

    return render(request, 'game_info_part/add_article.html', {'title': 'Добавление статьи', 'form': form})
