from rest_framework import serializers
from .models import User, Post, Like

class GetalluserSerializer(serializers.ModelSerializer):
  
    class Meta:
        model= User
        fields=('id','username','email','mobile','address')
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','mobile','address','password')
        write_only_fields = ('password',)
        extra_kwargs = {
            
            "email":{"required":True},
        }
    def create(self,validated_data):
        user=User(
            username=validated_data['username'],
            email=validated_data['email'],
            mobile=validated_data['mobile'],
            address=validated_data['address'],
            
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    like_count = serializers.SerializerMethodField()
   

    def get_like_count(self, obj):
        return obj.get_like_count()

    class Meta:
        model = Post
        fields = '__all__'

class PostpSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ('title','description','content')

class PostPutSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ('title','description','content')

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id','post']