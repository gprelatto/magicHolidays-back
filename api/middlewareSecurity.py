from .models import token, user
from datetime import date
from rest_framework import permissions

class checkAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.path_info != '/login/':
            try:
                userMail = request.headers['mail']
                userToken = request.headers['token']
                try:
                    oUser = user.objects.get(mail = userMail)
                    today = date.today()
                    try:
                        obj = token.objects.get(user = oUser.id,date = today, token = userToken)
                        return True
                    except token.DoesNotExist:
                        return False
                except user.DoesNotExist:
                    return False
            except:
                return False
        else:
            return True

