from django.contrib import admin
from django.urls import path, include
from User.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), #유저 관련 url 추가
    path('', home, name='home'),
]
