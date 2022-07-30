from django.urls import path

from game_info_part.views import HomePage, RegisterUser, LoginUser, logout_user, ShowArticle


urlpatterns = [path('', HomePage.as_view(), name="home"),
               path('registration/', RegisterUser.as_view(), name="register"),
               path('login/', LoginUser.as_view(), name="login"),
               path('logout/', logout_user, name="logout"),
               path('<slug:article_slug>/', ShowArticle.as_view(), name="article")
               ]
