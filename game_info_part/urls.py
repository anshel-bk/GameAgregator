from django.urls import path

from game_info_part.views import HomePage

urlpatterns = [path('',HomePage.as_view(),name="home")]