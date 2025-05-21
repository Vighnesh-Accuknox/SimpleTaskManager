from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authenticator = JWTAuthentication()

    def __call__(self, request):
        path = request.path
        method = request.method

        if path.startswith('/api/projects') or path.startswith('/api/tasks'):
            try:
                user_auth_tuple = self.jwt_authenticator.authenticate(request)
                if user_auth_tuple is None:
                    return JsonResponse({'detail': 'Authentication credentials de.'}, status=401)

                request.user = user_auth_tuple[0]  

                if path.startswith('/api/projects') and method != 'GET':
                    if not request.user.is_superuser:
                        return JsonResponse({'detail': 'Only admins can perform this action.'}, status=403)

            except Exception as e:
                return JsonResponse({'detail': 'Invalid or expired token.'}, status=401)
        response = self.get_response(request)
        return response
