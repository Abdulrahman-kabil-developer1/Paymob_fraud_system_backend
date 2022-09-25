from rest_framework import serializers
from .models import Blacklist,GlobalBlacklist, GlobalWhitelist, Review,Whitelist,Transaction
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
class TransctionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields=('id','name','email','phone','card_num','ip','merchant','amount','third_secure','created_at','transaction_status','rule','message')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=('id','reviewed','review_action','reviewed_at','name','email','phone','card_num','ip','merchant','amount','third_secure','created_at','transaction_status','rule','message')

class BlacklistSerializer(serializers.ModelSerializer):
    class Meta:
        model=Blacklist
        fields=('id','type','name','card_num','email','phone','ip','merchant','created_at','active')
        #optional type
        exstra_kwargs={'type':{'required':False}}

class GlobalBlacklistSerializer(serializers.ModelSerializer):
    class Meta:
        model=GlobalBlacklist
        fields=('id','type','name','card_num','email','phone','ip','created_at','active')
        exstra_kwargs={'type':{'required':False}}

class WhitelistSerializer(serializers.ModelSerializer):
    class Meta:
        model=Whitelist
        fields=('id','type','name','card_num','email','phone','ip','merchant','created_at','active')
        exstra_kwargs={'type':{'required':False}}

class GlobalWhitelistSerializer(serializers.ModelSerializer):
    class Meta:
        model=GlobalWhitelist
        fields=('id','type','name','card_num','email','phone','ip','created_at','active')
        exstra_kwargs={'type':{'required':False}}

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    class Meta:
        fields = ('username','email', 'first_name', 'last_name')

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    class Meta:
        fields = ('old_password','password','confirm_password')
    def validate(self, attrs):
        password=attrs.get('password')
        password1=attrs.get('confirm_password')
        if len(password)<8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        if password!=password1:
            raise serializers.ValidationError("Passwords must match")
        return attrs
    
    
    
    
    
    