from django.shortcuts import render
from ratelimit.decorators import ratelimit
from django.http import HttpResponse

@ratelimit(key='user_or_ip', rate=lambda request: '10/m' if request.user.is_authenticated else '5/m', block=True)
def login_view(request):
    return HttpResponse('<h1>Login</h1><p>This is the login page.</p>')
