from pickle import TRUE
import random
from datetime import datetime, timedelta


from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User

from core.models.Patient import Patient
from core.serializers.UserSerializer import  UserSerializer
from core.serializers.PatientSerializer import  PatientSerializer

# utils.py
from core.models.AssignedRule import AssignedRule
from CGM.models.CGMInput import CGMInput


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.dateparse import parse_date
 


def user_has_role(user, role_name):
    return AssignedRule.objects.filter(user=user, role__name=role_name).exists()
   

@api_view(['POST'])
def signup(request):
    # Check if username already exists
    if User.objects.filter(username=request.data['username']).exists():
        return Response({'username': ['A user with that username already exists.']}, status=status.HTTP_400_BAD_REQUEST)

    # Ensure mobile number is provided
    if 'mobile_number' not in request.data:
        return Response({'mobile_number': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)

    # Validate date format
    birthday = request.data.get('birthday')
    if birthday:
        try:
            parsed_birthday = parse_date(birthday)
            if parsed_birthday is None:
                return Response({'birthday': ['Invalid date format. It must be in YYYY-MM-DD format.']}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'birthday': ['Invalid date format. It must be in YYYY-MM-DD format.']}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the provided birthday and fallnumber exist in CGMInput
    fallnumber = request.data.get('fallnumber')

    if not CGMInput.objects.filter(birthday=birthday, fallnumber=fallnumber).exists():
        return Response({'detail': 'Invalid birthday or fallnumber.'}, status=status.HTTP_400_BAD_REQUEST)

    # Proceed with user creation
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        user.set_password(request.data['password'])
        user.save()
        
        patient_data = {
            'user': user.id,
            'birthday': birthday,
            'mobile_number': request.data['mobile_number'],  # Ensure mobile number is provided
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
def sendForgetPasswordCode(request):
    try:
        
  
        # Retrieve the associated patient object
        patient = Patient.objects.get(mobile_number=request.data['mobile_number'])
        
       
        # Generate a random verification code
        verification_code = str(random.randint(100000, 999999))
        
        # Update user's verification_code and sms_time_for_valid
        patient.verification_email_code = verification_code
        patient.verification_sms_code = verification_code
        patient.save()
        
        sendEmail(patient.user.email,verification_code)
         
        return Response({"message": ("Email verification code sent successfully.   " + patient.user.email)})

    except Patient.DoesNotExist:
        # If no patient object exists for the user, return an error response
        return Response({'error': 'No patient data found for this user'}, status=404)

 



from django.contrib.auth.hashers import make_password

@api_view(['POST'])
def sendCodeAndNewPassword(request):
    try:
        # Retrieve the associated patient object
        patient = Patient.objects.get(mobile_number=request.data['mobile_number'], verification_sms_code=request.data['verification_sms_code'])

        if patient:
            # Update the user's password
            patient.user.password = make_password(request.data['password'])
            patient.user.save()
            return Response({"message": "Password has been changed successfully."})
        else:
            return Response({"message": "Wrong mobile number or verification code."})

    except Patient.DoesNotExist:
        # If no patient object exists for the user, return an error response
        return Response({'message': 'No patient data found for this user'}, status=404)




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
def sendSmsVerification(request):
    # Retrieve the current user
    user = request.user
    
    # Assuming a OneToOneField relation between User and Patient
    try:
        # Retrieve the associated patient object
        patient = Patient.objects.get(user=user)
        
       
        # Generate a random verification code
        verification_code = str(random.randint(100000, 999999))
        
        # Update user's verification_code and sms_time_for_valid
        patient.verification_sms_code = verification_code
        patient.sms_time_for_valid = datetime.now() + timedelta(minutes=10)  # Set validity time to now + 10 minutes
        patient.save()
        
        # Send SMS with verification code (implement this part according to your SMS service provider's API)
        # send_sms(user.mobile_number, verification_code)  # You need to implement this function
        
        return Response({"message": "SMS verification code sent successfully."})

    except Patient.DoesNotExist:
        # If no patient object exists for the user, return an error response
        return Response({'error': 'No patient data found for this user'}, status=404)

  

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
        return Response({'error': 'No patient data found for this user'}, status=404)

        # If no patient object exists for the user, return an error response
   



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def sendEmailVerification(request):
    # Retrieve the current user
    user = request.user
    
    # Assuming a OneToOneField relation between User and Patient
    try:
        # Retrieve the associated patient object
        patient = Patient.objects.get(user=user)
        
       
        # Generate a random verification code
        verification_code = str(random.randint(100000, 999999))
        
        # Update user's verification_code and sms_time_for_valid
        patient.verification_email_code = verification_code
        patient.save()
        
        sendEmail(user.email,verification_code)
         
        return Response({"message": ("Email verification code sent successfully.   " + user.email)})

    except Patient.DoesNotExist:
        # If no patient object exists for the user, return an error response
        return Response({'error': 'No patient data found for this user'}, status=404)

 


def sendEmail(email, verification_code):
    subject = 'WZK Bestätigungscode'
    context = {'verification_code': verification_code}
    
    # Render HTML content from a template
    # html_content = render_to_string('core/templates/emails/email_template.html', context)
    html_content = render_to_string('emails/verification_email_template2.html', context)

    # Create a plain text version of the email (optional)
    text_content = strip_tags(html_content)
    
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    try:
        # Create an EmailMultiAlternatives object
        msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
        
        # Attach the HTML content to the email
        msg.attach_alternative(html_content, "text/html")
        
        # Send the email
        msg.send()
        
        print("Email has been sent! ")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False




@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def submitEmailVerification(request):
    try:
        user = request.user
        
        patient = Patient.objects.get(user=user)
        
        if patient.verification_email_code == request.data['verification_email_code'] :
            patient.is_email_verified = True
            patient.save()
            return Response({"message": "Email Verified!"})
        # else :
        #     return Response({"message": patient.verification_email_code})    



    except get_user_model().DoesNotExist:
        return Response("Not verified 1", status=status.HTTP_404_NOT_FOUND)
    return Response("Not verified ", status=status.HTTP_404_NOT_FOUND)

 



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    if not user_has_role(request.user, 'admin'):
        return Response({'message': 'No access'}, status=status.HTTP_403_FORBIDDEN)

    return Response({'message': 'User has admin role'})
