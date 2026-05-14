from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.conf import settings

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        if getattr(settings, 'MAINTENANCE_MODE', False):
            if not request.user.is_staff:
                return HttpResponse(""" 
                    <html>
                        <body style="text-align: center; padding: 20px; bg-color: red;">
                            <h1>Site is under maintenance</h1>
                            <p>Please check back later.</p>
                        </body>
                    </html> 
                    """, 
                    status=503, 
                    content_type='text/html')
        response = self.get_response(request)
        return response
    
class StaffAreaMiddleware:
    PROTECTED_PREFIX = '/Staff/'
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        if request.path.startswith(self.PROTECTED_PREFIX):
            #Step 1 - Authentication check
            # request.user is checked by AuthenticationMiddleware
            if not request.user.is_authenticated:
                login_url = getattr(settings, 'LOGIN_URL', '/accounts/login')
                return redirect(f'{login_url}?next={request.path}')
            
            #Step 2 - Authenticate check (groups or superuser)
            is_editor = request.user.groups.filter(name = 'Editors').exits()
            if not (is_editor or request.user.is_superuser):
                return HttpResponseForbidden(
                    
                )
            