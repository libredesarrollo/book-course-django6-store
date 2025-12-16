from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

@api_view(['POST'])
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
   
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response("User is invalid")
   
    pwd_valid = check_password(password, user.password)
    if not pwd_valid:
        return Response("Password is invalid")
   
    token,_ = Token.objects.get_or_create(user=user) # token, created(bool)
    print(Token.objects.get_or_create(user=user))
    return Response(token.key)