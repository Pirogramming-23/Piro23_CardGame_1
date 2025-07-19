// 카드 선택 라디오 버튼과 상대 드롭다운, Attack 버튼이 있다고 가정

document.addEventListener('DOMContentLoaded', function () {
    // 카드 선택
    let selectedCard = null;
    document.querySelectorAll('input[name="card"]').forEach(function (radio) {
        radio.addEventListener('change', function () {
            selectedCard = this.value;
        });
    });

    // 상대 선택
    let selectedDefender = null;
    document.getElementById('defender-select').addEventListener('change', function () {
        selectedDefender = this.value;
    });

    // Attack 버튼 클릭
    document.getElementById('attack-btn').addEventListener('click', function (e) {
        e.preventDefault();

        if (!selectedCard) {
            alert('카드를 선택하세요!');
            return;
        }
        if (!selectedDefender) {
            alert('상대를 선택하세요!');
            return;
        }

        // 서버로 POST 요청 (Django view에 맞게 URL/데이터 수정)
        fetch('/start_game/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken'), // CSRF 토큰 필요
            },
            body: `selected_card=${selectedCard}&defender=${selectedDefender}`
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            } else {
                return response.json();
            }
        })
        .then(data => {
            if (data && data.status === 'created') {
                alert('게임이 시작되었습니다!');
                // 필요시 페이지 이동
            }
        })
        .catch(error => {
            alert('에러 발생: ' + error);
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
