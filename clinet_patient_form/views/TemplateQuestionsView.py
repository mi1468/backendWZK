import json
from lib2to3.pgen2.token import EQUAL
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from clinet_patient_form.models.AnswerTemplateQuestions import AnswerTemplateQuestions
from ..models.Questions import Questions
from ..serializers.QuestionsSerializer import QuestionsSerializer
from django.db.models import Max
from django.db.models import Max, Case, When, Exists, OuterRef
from django.db.models import Max, OuterRef, Subquery
from rest_framework.request import Request
from django.http import JsonResponse
# from ..static.samples import templateFrom


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
 
def get_template_questions(request):
    user = request.user

    # Get the maximum page among active questions
    max_page = Questions.objects.filter(active=True).aggregate(max_page=Max('page'))['max_page']
    # curent_page = AnswerTemplateQuestions.objects.filter(user=request.user).aggregate(max_page=Max('page'))['max_page']
    current_page = Questions.objects.filter(type="text", answertemplatequestions__user=user, answertemplatequestions__answer_text__isnull=False, ).aggregate(Max('page'))
    if current_page["page__max"] is  None:
        current_page["page__max"] = 1

    # Get all template questions with user's answers
    template_questions = Questions.objects.filter(active=True).order_by('order')

    # Pass the request object to the serializer context
    serializer = QuestionsSerializer(template_questions, many=True, context={'request': request})

    return Response({'max_page': max_page, 'current_page':current_page["page__max"] , 'questions': serializer.data })



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
 
def get_template_questions_cgm(request):
    user = request.user

    # Get the maximum page among active questions
    # try:

    with open('core/static/samples/templateForm.json', 'r') as json_file:
        template_data = json.load(json_file)
    # with open('template_form.json', 'r') as json_file:
    #     template_data = templateFrom.load(json_file)
    return JsonResponse(template_data)
    # except FileNotFoundError:
    #     return JsonResponse({'error': 'Template form JSON file not found'}, status=404)
    # except Exception as e:
        # return JsonResponse({'error': str(e)}, status=500)
    # return Response({'max_page': max_page, 'current_page':current_page["page__max"] , 'questions': serializer.data })



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_template_pages(request):
    # Get the maximum page among active questions
    max_page = Questions.objects.filter(active=True).aggregate(max_page=Max('page'))['max_page']
    
    # Return the maximum page value in the response
    return Response({'max_page': max_page})