import re
from django.core.exceptions import ValidationError
from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Ensure username matches the following conditions:
    #   1. Alphanumeric or single hyphens
    #   2. Does not start or end with a hyphen
    username_pattern = r'(?<!^-)[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*(?<!-)$'

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def validate(self, data):
        user = User(**data)
        password = data.get('password', user)
        try:
            validate_password(password)
        except ValidationError as e:
            serializer_errors = serializers.as_serializer_error(e)
            raise serializers.ValidationError({'password': serializer_errors['non_field_errors']})
        
        return data

    def validate_username(self, username):
        if len(username) < 5:
            raise serializers.ValidationError('Username must be at least 5 characters long.')

        if username.startswith('-'):
            raise serializers.ValidationError('Username may not start with \'-\'.')

        if username.endswith('-'):
            raise serializers.ValidationError('Username may not end with \'-\'.')

        #   1. Alphanumeric or single hyphens
        #   2. Does not start or end with a hyphen
        if re.match(self.username_pattern, username) is None:
            raise serializers.ValidationError('Username may only contain letters, numbers, or single hyphens.')

        if User.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError('User with this username already exists.')
        
        return username

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            username = validated_data['username'],
            password = validated_data['password']
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
