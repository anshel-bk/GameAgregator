from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import SuspiciousOperation

from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse_lazy

from .forms import RegisterUserForm, LoginUserForm, AddArticleForm, ChangeRating, CommentForm
from .models import Article, Comment
from django.views.generic import TemplateView, CreateView, ListView

from .services.change_rating import change_rating_func
from .services.form_data import adding_necessary_data
from .services.search_module import search_by_all


class HomePage(ListView):
    template_name = "game_info_part/home.html"
    paginate_by = 6
    model = Article

    def get_context_data(self, **kwargs):
        articles = Article.objects.filter(is_published=True).order_by('rating').reverse()
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
        comment_form = CommentForm()
        data = Article.objects.get(slug=article_slug)
        form_rating = ChangeRating()
        context = {"data": data, "title": data.title, "form": form_rating,"comment_form":comment_form}
        return context

    def post(self, request, article_slug, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            text = request.POST['text']
            username = self.request.user
            post = get_object_or_404(Article, slug=article_slug)
            comment = Comment.objects.create(post=post, username=username, text=text)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return redirect('article')


@login_required
def add_article(request):
    if request.method == 'POST':
        form = AddArticleForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                data = adding_necessary_data(form.cleaned_data, request)
                Article.objects.create(**data)
                return redirect('home')
            except SuspiciousOperation:
                form.add_error(None, f"Ошибка добавления статьи")
    else:
        form = AddArticleForm()

    return render(request, 'game_info_part/add_article.html', {'title': 'Добавление статьи', 'form': form})


def user_profile(request):
    username = request.user.username
    context = {"title": f"Страница пользователя {username}", 'username': username}
    return render(request, 'game_info_part/user_profile.html', context)


def search(request):
    search_value = request.POST.get("search_value")
    search_results = search_by_all(search_value)
    if not search_results:
        template = 'game_info_part/empty_search.html'
    else:
        template = 'game_info_part/search.html'
    context = {"title": f"Результаты поиска по запросу {search_value} ",
               "articles": search_results}
    return render(request, template_name=template, context=context)


@login_required
def change_rating(request, article_slug):
    user = request.user.username
    grade = request.POST['rating']
    change_rating_func(user, article_slug, grade)
    return redirect('article', article_slug=article_slug)


def pageNotFound(request, exception):
    return render(request, 'game_info_part/handler_404.html')
