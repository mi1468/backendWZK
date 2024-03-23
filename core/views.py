from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# from .models.user import User
from django.contrib.auth.models import User

from .serializers.UserSerializer import UserSerializer

# from .serializers.user import UserSerializer



# utils.py
from .models.AssignedRule import AssignedRule

def user_has_role(user, role_name):
    return AssignedRule.objects.filter(user=user, role__name=role_name).exists()
   


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    try:
        user = get_user_model().objects.get(email=request.data['email'])
    except get_user_model().DoesNotExist:
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)

    if not user.check_password(request.data['password']):
        return Response("Invalid password", status=status.HTTP_401_UNAUTHORIZED)

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    if not user_has_role(request.user, 'admin'):
        return Response({'message': 'No access'}, status=status.HTTP_403_FORBIDDEN)

    return Response({'message': 'User has admin role'})
