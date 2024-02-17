from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserSerialzer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'phonenumber', 'profileImage', 'id']
        extra_kwargs = {'password' : {'write_only' : True}}

    def validate_passeord(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value


    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user