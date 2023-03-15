from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import User, Post, Comment
from .permissions import PermissionUser, PermissionPolicyMixin
from .serializers import UserSerializer, PostWriteSerializer, PostReadSerializer, \
    CommentWriteSerializer, CommentReadSerializer


class UserViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes_per_method = {
        'list': [IsAuthenticated],
        'create': [AllowAny],
        'update': [PermissionUser],
        'destroy': [IsAdminUser],
        'retrieve': [IsAuthenticated]
    }


class PostViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Post.objects.all()
    permission_classes_per_method = {
        'list': [AllowAny],
        'create': [IsAuthenticated],
        'update': [PermissionUser],
        'destroy': [PermissionUser],
        'retrieve': [AllowAny]
    }

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return PostWriteSerializer
        return PostReadSerializer


class CommentViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes_per_method = {
        'list': [AllowAny],
        'create': [IsAuthenticated],
        'update': [PermissionUser],
        'destroy': [PermissionUser],
        'retrieve': [AllowAny]
    }

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CommentWriteSerializer
        return CommentReadSerializer
