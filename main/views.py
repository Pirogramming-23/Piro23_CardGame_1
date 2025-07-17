# views.py
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Game, User
from django.contrib.auth.decorators import login_required


@login_required
def start_game_view(request):
    if request.method == 'POST':
        selected_card = int(request.POST.get('selected_card'))
        defender_id = request.POST.get('defender')
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
    # 자신이 공격한 게임
    my_attacks = Game.objects.filter(attacker=user).order_by('-created_at')  # type: ignore
    # 자신이 수비자인 게임
    my_defenses = Game.objects.filter(defender=user).order_by('-created_at')  # type: ignore
    context = {
        'my_attacks': my_attacks,
        'my_defenses': my_defenses,
    }
    return render(request, 'game_list.html', context)

def game_list(request):
    return render(request, 'game_list.html')

def home(request):
    return render(request, 'home.html')
