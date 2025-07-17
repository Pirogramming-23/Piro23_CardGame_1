# urls.py
from django.urls import path
from .views import home, start_game_view, game_list

urlpatterns = [
    path('', home, name='home'),
    path('start_game/', start_game_view, name='start_game'),
    path('game-list/', game_list, name='game_list'),
]