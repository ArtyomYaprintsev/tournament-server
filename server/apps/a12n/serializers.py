from django.core import serializers
from apps.acсount.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password',},
        min_length=8,
        )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password',},
        lable='Confirm password',
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'lastname',
            'password',
            'password_confirm',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('Passwords dont match')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user