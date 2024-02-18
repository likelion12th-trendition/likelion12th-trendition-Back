from .models import *
from django.contrib.auth.password_validation import validate_password 
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator


#회원가입
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    phonenumber = serializers.CharField(required=True)

    class Meta: 
        model = CustomUser
        fields = ('username', 'password', 'email', 'phonenumber')

    def create(self, validated_data): 
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phonenumber=validated_data['phonenumber'],
        )
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)       
        return user

#로그인
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data) 
        if user:
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError( #User가 None인 경우
            {"error": "해당하는 사용자가 존재하지 않습니다."})


#마이페이지
class MyPageSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['username', 'followers', 'followings']

    def get_followers(self, obj):
        return obj.follower.count()

    def get_followings(self, obj):
        return obj.following.count()