import re

from django.utils import timezone
from rest_framework import serializers

from .models import User, Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'post', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'phone_number', 'date_of_birth',
                  'date_created', 'date_updated']

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(user.password)
        user.save()
        return user

    def validate_password(self, value):
        if len(value) < 8 or not re.search(r'\d', value):
            raise serializers.ValidationError("Password must be at least 8 characters and contain at least 1 digit.")
        return value

    def validate_email(self, value):
        allowed_domains = ('mail.ru', 'yandex.ru')
        domain = value.split('@')[-1]
        if domain not in allowed_domains:
            raise serializers.ValidationError("Only mail.ru and yandex.ru email addresses are allowed.")
        return value


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'image', 'author', 'comments', 'created_at', 'updated_at']

    def validate_title(self, value):
        forbidden_words = ['ерунда', 'глупость', 'чепуха']
        for word in forbidden_words:
            if word in value.lower():
                raise serializers.ValidationError(f"The word '{word}' is not allowed in the title.")
        return value

    def validate_author(self, value):
        if not value.is_staff:
            if value.date_of_birth is None:
                raise serializers.ValidationError("Author's date of birth is not specified.")
            age = (timezone.now().date() - value.date_of_birth).days // 365
            if age < 18:
                raise serializers.ValidationError("Only users who have reached the age of 18 can create posts.")
            return value
        return value
