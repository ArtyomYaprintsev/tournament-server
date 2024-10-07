from rest_framework import serializers
from .models import User, Team


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    avatar = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'full_name',
            'avatar',
        ]

    def get_full_name(self, obj) -> str:
        return f'{obj.first_name} {obj.last_name}'


class UserDetailSerializer(UserSerializer):
    full_name = serializers.SerializerMethodField()
    avatar = serializers.ImageField(required=False, allow_null=True)
    class Meta(UserSerializer.Meta):
        model = User
        fields = UserSerializer.Meta.fields + [
            'gender',
            'is_verified',
            'rating'
        ]
        
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'avatar',
        ]

    def update(self, instance, validated_data):
        instance.username = validated_data.get(
            'username',
            instance.username
        )
        instance.first_name = validated_data.get(
            'first_name',
            instance.first_name
        )
        instance.last_name = validated_data.get(
            'last_name',
            instance.last_name
        )
        avatar = validated_data.get('avatar', None)
        if avatar:
            instance.avatar = avatar
        instance.save()
        return instance