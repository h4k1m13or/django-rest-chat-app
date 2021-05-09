import datetime
from django.conf import settings
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from .models import UserProfile





class ActiveUserMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
       
        current_user = request.user 
        now = datetime.datetime.now()
        if request.user.is_authenticated:
            try:
                UserProfile.objects.get(user=current_user)
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=current_user)
            finally:
                cache.set('last_seen_%s' % current_user.username, now,
                        settings.USER_LASTSEEN_TIMEOUT)
            
            cache.set('seen_%s' % current_user.username, now,
                      settings.USER_LASTSEEN_TIMEOUT)
