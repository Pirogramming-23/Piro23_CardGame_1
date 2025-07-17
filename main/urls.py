# urls.py
from django.urls import path
from .views import home, start_game_view, game_list, counter_attack_view, game_detail_view

urlpatterns = [
    path('', home, name='home'),
    path('start_game/', start_game_view, name='start_game'),
    path('game-list/', game_list, name='game_list'),
    path('counter-attack/<int:game_id>/', counter_attack_view, name='counter_attack'),
     path('games/<int:game_id>/', game_detail_view, name='game_detail'),
]