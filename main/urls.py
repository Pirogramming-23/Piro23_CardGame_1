# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('start_game/', views.start_game_view, name='start_game'),
    path('game_list/', views.game_list_view, name='game_list'),
]