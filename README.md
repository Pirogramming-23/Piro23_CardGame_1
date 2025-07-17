# Piro23_CardGame_1
피로그래머 카드게임 만들기 1조 레포지토리 입니다!!
<br>
## .env 파일 사용해서 SocialApp, Sites 등록 안해도 소셜 로그인 되게 하는법
1. git clone 을 이용해 클론 받기
2. 프로젝트의 루트 디렉토리 (manage.py 있는 곳) 에서 .env 파일 만들기
3. 카톡에 보내준 양식 그대로 붙여넣기
4. python -m venv venv 로 가상환경 설정하기
5. pip install -r requirements.txt 이용해서 필요한 패키지 모두 설치
6. python manage.py makemigrations 로 db 만들기
> 이때 만약 오류나는 경우, pip uninstall django 로 장고를 지웠다가 pip install django로 재설치 해주자. 장고가 제대로 설치되지 않으면 이런 문제가 생긴다.
7. python manage.py migrate 로 모델 올리기
8. python manage.py runserver 로 로그인 잘 되는지 확인하기
