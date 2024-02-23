import logging

from rest_framework import status, generics
from rest_framework.response import Response
from .authentication import BearerTokenAuthentication

from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *

# Create your views here.

#회원가입
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

#로그인
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    # authentication_classes = [BearerTokenAuthentication]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response({"token": data['token'].key, "username": data['username']}, status=status.HTTP_200_OK)



#팔로잉
class FollowView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    def get(self, request, username):  
        if request.user.is_authenticated:
            you = get_object_or_404(CustomUser, username=username)
            me = request.user
            if you in me.following.all():
                return Response("팔로우 상태입니다.", status=status.HTTP_200_OK)
            else:
                return Response("언팔로우 상태입니다.", status=status.HTTP_200_OK)
        else:
            return Response("로그인이 필요한 서비스입니다.", status=status.HTTP_401_UNAUTHORIZED)
    def post(self, request, username):
        if request.user.is_authenticated:
            you = get_object_or_404(CustomUser, username=username)  
            me = request.user

            if you in me.following.all():
                me.following.remove(you)
                you.follower.remove(me)
                return Response("언팔로우 했습니다.", status=status.HTTP_200_OK)
            else:
                me.following.add(you)
                you.follower.add(me)
                return Response("팔로우 했습니다.", status=status.HTTP_200_OK)
        else:
            return Response("로그인이 필요한 서비스입니다.", status=status.HTTP_401_UNAUTHORIZED)

#마이페이지
class MyPageView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    def get(self, request):
        if request.user.is_authenticated:
            serializer = MyPageSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response({'error': '로그인이 필요한 서비스입니다.'})
        
#내가 팔로우하는 유저 목록
class FollowingUsersView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    def get(self, request, *args, **kwargs):
        following_users = [{'username': user.username, 'profileImage': user.profileImage.url} for user in request.user.following.all()] 
        return Response(following_users)

#나를 팔로우하는 유저 목록
class FollowerUsersView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    def get(self, request, *args, **kwargs):
        follower_users = [{'username': user.username, 'profileImage': user.profileImage.url} for user in request.user.follower.all()] 
        return Response(follower_users)
    
#검색
class SearchView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    def get(self, request): 
        users = CustomUser.objects.all()
        user_data = [{'username': user.username, 'profileImage': user.profileImage.url} for user in users]
        return Response(user_data)


#유저 검색
class SearchUserView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    def get(self, request): 
        keyword = request.query_params.get('keyword')  
        if keyword:
            users = CustomUser.objects.filter(username__icontains=keyword)  
            if users.exists(): 
                serializer = MyPageSerializer(users, many=True)
                return Response(serializer.data)
            else:  
                return Response({"error": "해당 유저는 존재하지 않습니다."})
        else:
            return Response({"error": "검색어가 없습니다."})



