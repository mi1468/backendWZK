 

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# from .models.user import User
from django.contrib.auth.models import User

# from .serializers.user import UserSerializer
from ..serializers.PatientSerializer import  PatientSerializer
from ..serializers.UserSerializer import  UserSerializer

# utils.py
from ..models.AssignedRule import AssignedRule
from ..models.Patient import Patient

def user_has_role(user, role_name):
    return AssignedRule.objects.filter(user=user, role__name=role_name).exists()
   


@api_view(['POST'])
def signup(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        user.set_password(request.data['password'])
        user.save()
        
        patient_data = {
            'user': user.id,
            'birthday': request.data['birthday'],
            
        }
        patient_serializer = PatientSerializer(data=patient_data)
        if patient_serializer.is_valid():
            patient_serializer.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': patient_serializer.data}, status=status.HTTP_201_CREATED)
        else:
            # If patient data is invalid, delete the created user
            user.delete()
            return Response(patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)





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
def getInfo(request):
    # Retrieve the current user
    user = request.user
    
    # Assuming a OneToOneField relation between User and Patient
    try:
        # Retrieve the associated patient object
        patient = Patient.objects.get(user=user)
        
        # Serialize the patient data
        serializer = PatientSerializer(patient)
        
        # Return the serialized patient data
        return Response(serializer.data)
    except Patient.DoesNotExist:
        # If no patient object exists for the user, return an error response
        return Response({'error': 'No patient data found for this user'}, status=404)


        

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    if not user_has_role(request.user, 'admin'):
        return Response({'message': 'No access'}, status=status.HTTP_403_FORBIDDEN)

    return Response({'message': 'User has admin role'})
