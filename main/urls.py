# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('start_game/', start_game_view, name='start_game'),
    # 기존 game_list 뷰 함수를 사용하도록 수정했습니다.
    path('game-list/', game_list, name='game_list'), 
    path('counter-attack/<int:game_id>/', counter_attack_view, name='counter_attack'),
    
    # [추가] 게임 상세 페이지 URL
    path('game/<int:game_id>/', game_detail_view, name='game_detail'),
    # [추가] 게임 취소 URL
    path('game/<int:game_id>/cancel/', cancel_game_view, name='cancel_game'),
]