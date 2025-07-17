# views.py
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Game, User
from django.contrib.auth.decorators import login_required


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
def game_list_view(request):
    user = request.user
    my_attacks_qs = Game.objects.filter(attacker=user).order_by('-created_at')  # type: ignore
    my_defenses_qs = Game.objects.filter(defender=user).order_by('-created_at')  # type: ignore
    my_attacks = [(game, game.can_counter(user)) for game in my_attacks_qs]
    my_defenses = [(game, game.can_counter(user)) for game in my_defenses_qs]
    context = {
        'my_attacks': my_attacks,
        'my_defenses': my_defenses,
    }
    return render(request, 'game_list.html', context)

def game_list(request):
    return render(request, 'game_list.html')

def home(request):
    return render(request, 'home.html')

@login_required
def counter_attack_view(request, game_id):
    game = get_object_or_404(Game, id=game_id, defender=request.user)
    if request.method == 'POST':
        selected_card = request.POST.get('selected_card')
        if not selected_card:
            return redirect('counter_attack', game_id=game_id)
        game.defender_card = int(selected_card)
        # 결과 계산: 승/패/무 랜덤 결정
        if game.attacker_card is not None and game.defender_card is not None:
            # 랜덤하게 승리 조건 결정 (높은 숫자 승/낮은 숫자 승)
            high_win = random.choice([True, False])
            if game.attacker_card == game.defender_card:
                # 무승부
                game.status = Game.Status.COMPLETED
                game.winner = None
                game.loser = None
                game.attacker_score_change = 0
                game.defender_score_change = 0
            else:
                if (high_win and game.attacker_card > game.defender_card) or (not high_win and game.attacker_card < game.defender_card):
                    # 공격자 승리
                    game.status = Game.Status.COMPLETED
                    game.winner = game.attacker
                    game.loser = game.defender
                    game.attacker_score_change = game.attacker_card
                    game.defender_score_change = -game.defender_card
                else:
                    # 수비자 승리
                    game.status = Game.Status.COMPLETED
                    game.winner = game.defender
                    game.loser = game.attacker
                    game.attacker_score_change = -game.attacker_card
                    game.defender_score_change = game.defender_card
            game.save()
        else:
            game.save()
        return redirect('game_list')
    # GET: 카드 5개 랜덤 생성 (1~10 중)
    card_choices = random.sample(range(1, 11), 5)
    return render(request, 'counter_attack.html', {
        'game': game,
        'card_choices': card_choices,
    })
