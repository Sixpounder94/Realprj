import re

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse



EXEMT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

class LoginRequairedMIddleware:
    def __init__(self, get_response):
        print(get_response)
        self.get_response = get_response


    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')

        path = request.path_info.lstrip('/')
        print(path)
        print(EXEMT_URLS)

        # if not request.user.is_authenticated():
        #     if not any(url.match(path) for url in EXEMT_URLS):
        #         return redirect(settings.LOGIN_REDIRECT_URL)

        url_is_exemt = any(url.match(path) for url in EXEMT_URLS)
       # print('loool' + reverse('logout'))
        if path == reverse('dairy:logout'):
            logout(request)

        if request.user.is_authenticated() and url_is_exemt:
            return redirect(settings.LOGIN_REDIRECT_URL)

        elif request.user.is_authenticated() or url_is_exemt:
            return None

        else:
            return redirect(settings.LOGIN_URL)
