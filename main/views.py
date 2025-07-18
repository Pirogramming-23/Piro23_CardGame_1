# views.py
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Game, User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q 

@login_required
def start_game_view(request):
    if request.method == 'POST':
        selected_card = request.POST.get('selected_card')
        defender_id = request.POST.get('defender')
        if not selected_card or not defender_id:
            return redirect('start_game')
        defender = get_object_or_404(User, id=defender_id)
        Game.objects.create( #type: ignore
            attacker=request.user,
            defender=defender,
            attacker_card=selected_card
        )
        return redirect('game_list')

    # GET 요청: 카드 5개 랜덤 생성 (1~10 중)
    card_choices = random.sample(range(1, 11), 5)
    defenders = User.objects.exclude(id=request.user.id)
    return render(request, 'start_game.html', {
        'card_choices': card_choices,
        'defenders': defenders
    })

@login_required
def game_list(request):
    user = request.user
    
    # --- 디버깅 코드 시작 ---
    print("\n" + "="*50)
    print(f"DEBUG: game_list 뷰 실행 확인")
    print(f"1. 현재 로그인 유저: {user.username} (ID: {user.id})")
    print(f"2. 데이터베이스의 전체 게임 수: {Game.objects.count()}")
    print(f"3. '{user.username}' 유저가 공격자로 포함된 게임 수: {Game.objects.filter(attacker=user).count()}")
    print(f"4. '{user.username}' 유저가 수비자로 포함된 게임 수: {Game.objects.filter(defender=user).count()}")
    print("="*50 + "\n")
    # --- 디버깅 코드 끝 ---

    my_attacks = Game.objects.filter(attacker=user, is_deleted_by_attacker=False).order_by('-created_at')
    defenses_qs = Game.objects.filter(defender=user, is_deleted_by_attacker=False).order_by('-created_at')

    my_defenses_with_status = []
    for game in defenses_qs:
        my_defenses_with_status.append({
            'game_object': game,
            'user_can_counter': game.can_counter(user)
        })

    context = {
        'my_attacks': my_attacks,
        'my_defenses': my_defenses_with_status,
    }
    return render(request, 'game_list.html', context)


def home(request):
    return render(request, 'home.html')

@login_required
def counter_attack_view(request, game_id):
    game = get_object_or_404(Game, id=game_id, defender=request.user)

    if game.status != Game.Status.PENDING:
        return redirect('game_list')

    if request.method == 'POST':
        selected_card = request.POST.get('selected_card')
        if not selected_card:
            return redirect('counter_attack', game_id=game_id)

        try:
            with transaction.atomic():
                game.defender_card = int(selected_card)
                game.status = Game.Status.COMPLETED

                high_card_wins = random.choice([True, False])

                if game.attacker_card == game.defender_card:
                    game.winner = None
                    game.loser = None
                    game.attacker_score_change = 0
                    game.defender_score_change = 0
                else:
                    attacker_wins = (high_card_wins and game.attacker_card > game.defender_card) or \
                                    (not high_card_wins and game.attacker_card < game.defender_card)

                    if attacker_wins:
                        game.winner = game.attacker
                        game.loser = game.defender
                        game.attacker_score_change = game.attacker_card
                        game.defender_score_change = -game.defender_card
                    else:
                        game.winner = game.defender
                        game.loser = game.attacker
                        game.attacker_score_change = -game.attacker_card
                        game.defender_score_change = game.defender_card
                
                # [수정] 유저 총점 업데이트 시 '.total_score' 필드를 사용합니다.
                if game.winner:
                    # 점수를 업데이트할 유저 객체를 명시적으로 다시 불러옵니다.
                    winner_user = User.objects.get(id=game.winner.id)
                    loser_user = User.objects.get(id=game.loser.id)

                    winner_user.total_score += abs(game.attacker_score_change if winner_user == game.attacker else game.defender_score_change)
                    loser_user.total_score += -abs(game.attacker_score_change if loser_user == game.attacker else game.defender_score_change)
                    
                    winner_user.save()
                    loser_user.save()

                game.save()

        except Exception as e:
            print(f"Error during counter attack: {e}")
            return redirect('game_list')

        return redirect('game_list')

    card_choices = random.sample(range(1, 11), 5)
    return render(request, 'counter_attack.html', {
        'game': game,
        'card_choices': card_choices,
    })

@login_required
def game_detail_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    # 현재 로그인한 유저가 이 게임의 공격자인지 확인
    is_attacker = (game.attacker == request.user)
    # 현재 로그인한 유저가 게임을 취소할 수 있는지 확인 (모델 메서드 활용)
    user_can_cancel = game.can_cancel(request.user)
    user_can_counter = game.can_counter(request.user) # [추가]

    context = {
        'game': game,
        'is_attacker': is_attacker,
        'user_can_cancel': user_can_cancel,
        'user_can_counter': user_can_counter,
    }
    return render(request, 'game_detail.html', context)

# [추가] 게임 취소 뷰
@login_required
def cancel_game_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if game.can_cancel(request.user):
        # is_deleted_by_attacker 플래그를 True로 변경
        game.is_deleted_by_attacker = True
        game.save()
    return redirect('game_list')
