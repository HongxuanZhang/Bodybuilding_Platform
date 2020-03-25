from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import *

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'tag', 'description')

class CourseQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class RegSerializers(serializers.ModelSerializer):
    confirmpwd = serializers.CharField(max_length=256, min_length=4, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'tel', 'age', 'sex', 'confirmpwd')

    def validate(self, attrs):
        if attrs['confirmpwd'] != attrs['password']:
            raise ValidationError('两次密码输入不一致')
        del attrs['confirmpwd']
        attrs['password'] = make_password(attrs['password'])
        attrs['status'] = "Normal"
        return attrs

class LogSerializers(serializers.ModelSerializer):
    username = serializers.CharField(max_length=6)

    class Meta:
        model = User
        fields = ('username', 'password', 'isAdmin')

    def validate(self, attrs):
        user_obj = User.objects.filter(username=attrs['username']).first()
        if user_obj:
            if check_password(attrs['password'], user_obj.password) and user_obj.status == 'Normal':
                return attrs
            elif user_obj.status != 'Normal':
                raise ValidationError('账号状态异常，请申请解冻')
            elif user_obj.isAdmin != attrs['isAdmin']:
                raise ValidationError('用户名或密码错误')
        raise ValidationError('用户名或密码错误')

class UserListSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'tel', 'age', 'sex', 'status', 'last_login', 'date_joined')

