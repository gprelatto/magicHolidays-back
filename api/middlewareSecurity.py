from .models import token, user
from datetime import date
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer

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






class CustomJsonRender(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):

        if renderer_context:
            response = renderer_context['response']
            code = response.status_code
            msg = "OK"
            if isinstance(data, dict):
                code = data.pop('code', code)
                msg = data.pop('message', msg)
                data = data.pop('data', data)
            if code != 200 and data:
                msg = data.pop('detail', 'failed')
            response.status_code = 200
            res = {
                'code': code,
                'message': msg,
                'data': data,
            }
            return super().render(res, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)