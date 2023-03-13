from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from .models import User, Post, Comment
from .permissions import PermissionOrOwner, PermissionPolicyMixin
from .serializers import UserSerializer, PostSerializer, CommentSerializer


class UserViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes_per_method = {
        'list': [AllowAny],
        'create': [AllowAny],
        'update': [PermissionOrOwner],
        'destroy': [IsAdminUser],
        'retrieve': [PermissionOrOwner]
    }


class PostViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes_per_method = {
        'list': [AllowAny],
        'create': [IsAuthenticated],
        'update': [PermissionOrOwner],
        'destroy': [PermissionOrOwner],
        'retrieve': [PermissionOrOwner]
    }


class CommentViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes_per_method = {
        'list': [AllowAny],
        'create': [PermissionOrOwner],
        'update': [PermissionOrOwner],
        'destroy': [PermissionOrOwner],
        'retrieve': [PermissionOrOwner]
    }



