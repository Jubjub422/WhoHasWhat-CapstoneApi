from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from whohaswhatapi.models import Lender


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''
    username = request.data['username']
    password = request.data['password']
    authenticated_user = authenticate(username=username, password=password)

    if authenticated_user is not None:
        lender_user = Lender.objects.get(user=authenticated_user)
        token = Token.objects.get(user=authenticated_user)
        if lender_user.active is True:
            data = {
                'valid': True,
                'token': token.key
            }
        else:
            data = {'valid': False}
        return Response(data)
    else:

        data = {'valid': False}
        return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    new_user = User.objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name']

    )

    lender_user = Lender.objects.create(
        profile_image_url=request.data['profile_image_url'],
        user=new_user,
        address=request.data['address'],
        is_owner=request.data['is_owner'],
        is_renter=request.data['is_renter']
    )

    token = Token.objects.create(user=lender_user.user)
    data = {'token': token.key}
    return Response(data)
