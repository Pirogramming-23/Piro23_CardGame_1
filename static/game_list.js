document.addEventListener('DOMContentLoaded', function () {
    // 취소 버튼 클릭
    document.querySelectorAll('.cancel-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const gameId = this.dataset.gameId;
            if (confirm('정말로 이 게임을 취소하시겠습니까?')) {
                fetch(`/cancel_game/${gameId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                    }
                })
                .then(response => {
                    if (response.ok) {
                        alert('게임이 취소되었습니다.');
                        location.reload();
                    } else {
                        alert('취소 실패');
                    }
                });
            }
        });
    });

    // CounterAttack 버튼 클릭
    document.querySelectorAll('.counter-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            // counter_attack.html로 이동
            window.location.href = '/main/templates/counter_attack.html';
        });
    });

    // CSRF 토큰 가져오기 함수 (Django용)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
