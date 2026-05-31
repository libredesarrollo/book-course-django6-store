from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import resolve, Resolver404

class DemoModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        
        # 1. Allow standard reading GET, HEAD, OPTIONS, TRACE requests.
        # But we must intercept GET requests that perform database deletions/writes.
        if request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            # Check if this is a delete/add/update/create action triggered via GET request
            try:
                match = resolve(path)
                view_name = match.view_name
            except Resolver404:
                view_name = ""

            # Check for known GET-based modifying routes (e.g., elements delete)
            is_destructive_get = (
                'delete' in view_name.lower() or 
                'delete' in path.lower() or 
                'remove' in path.lower() or
                'destroy' in path.lower()
            )
            
            # Exclude admin dashboard or other safe read-only routes containing 'delete'
            if is_destructive_get and not path.startswith('/admin/'):
                return self.handle_blocked_write(request)

            return self.get_response(request)

        # 2. For non-safe methods (POST, PUT, PATCH, DELETE)
        # We MUST allow authentication endpoints (login, logout, and token request) to write session data
        allowed_auth_paths = [
            '/login',
            '/logout',
            '/accounts/login/',
            '/accounts/logout/',
            '/admin/login/',
            '/admin/logout/',
            '/api-token-auth/',
        ]
        
        # Check if the request is trying to authenticate
        is_auth_request = any(path.startswith(p) for p in allowed_auth_paths) or 'login' in path.lower() or 'logout' in path.lower()
        
        if is_auth_request:
            return self.get_response(request)

        # 3. Block any other mutating request (POST, PUT, PATCH, DELETE)
        return self.handle_blocked_write(request)

    def handle_blocked_write(self, request):
        message = "¡Modo Demo Activo! Las operaciones de creación, edición y eliminación de registros están desactivadas en este entorno."
        
        # If it's an AJAX or API request, return a clean JSON response
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.path_info.startswith('/api/'):
            return JsonResponse({
                'detail': message,
                'code': 'demo_mode_restriction'
            }, status=403)

        messages.warning(request, message)
        
        # Redirect back to the referrer, or home page if referrer is not present
        referrer = request.META.get('HTTP_REFERER')
        if referrer:
            return redirect(referrer)
        return redirect('/')
