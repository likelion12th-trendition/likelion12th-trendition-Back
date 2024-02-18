from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    
    path('follow/<str:username>/', FollowView.as_view(), name="follow_view"), #팔로우 버튼이랑 해당 URL 연결
    path('mypage/', MyPageView.as_view(), name="mypage_view"), #마이페이지
    path('following/', FollowingUsersView.as_view(), name='following-users'), #내가 팔로우하는 유저 목록
    path('follower/', FollowerUsersView.as_view(), name='follower-users'), #나를 팔로우하는 유저 목록
    path('search/', SearchView.as_view()), #검색 (/search/?keyword=유저네임 경로로 접속)
]
