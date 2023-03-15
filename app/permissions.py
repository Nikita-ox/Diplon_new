from rest_framework.permissions import BasePermission


class PermissionPolicyMixin:
    def check_permissions(self, request):
        try:
            handler = getattr(self, request.method.lower())
        except AttributeError:
            handler = None

        if handler and self.permission_classes_per_method and self.permission_classes_per_method.get(handler.__name__):
            self.permission_classes = self.permission_classes_per_method.get(handler.__name__)

        super().check_permissions(request)


class PermissionUser(BasePermission):
    message = 'Нет доступа: Вы не Администратор или не владелец данной учетной записи'

    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.author.id:
            return True
        elif request.user.is_staff:
            return True
        return False
