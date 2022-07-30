from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from .forms import RegisterUserForm, LoginUserForm
from .models import Article, AuthorArticle
from django.views.generic import TemplateView, CreateView, ListView


class HomePage(ListView):
    template_name = "game_info_part/home.html"
    paginate_by = 6
    model = Article

    def get_context_data(self, **kwargs):
        articles = Article.objects.filter(is_published=True)
        article_list = Article.objects.all()
        paginator = Paginator(articles,6)  # Show 25 contacts per page.

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
        context = {"form": RegisterUserForm}
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'game_info_part/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {"form": LoginUserForm}
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
