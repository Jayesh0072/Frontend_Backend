from datetime import datetime, timedelta

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the last activity time from the session
        last_activity = request.session.get('last_activity')
        now = datetime.now()

        # Set a timeout duration (e.g., 15 minutes)
        timeout = timedelta(minutes=1)

        if last_activity:
            last_activity_time = datetime.fromisoformat(last_activity)
            if now - last_activity_time > timeout:
                # Clear session if timeout is exceeded
                request.session.flush()
        
        # Update the last activity time
        request.session['last_activity'] = now.isoformat()

        response = self.get_response(request)
        return response

# from datetime import datetime, timedelta
# from django.conf import settings
# from django.contrib import auth

# class AutoLogout:
#   def process_request(self, request):
#     if not request.user.is_authenticated() :
#       #Can't log out if not logged in
#       return

#     try:
#       if datetime.now() - request.session['last_touch'] > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
#         auth.logout(request)
#         del request.session['last_touch']
#         return
#     except KeyError:
#       pass

#     request.session['last_touch'] = datetime.now()
