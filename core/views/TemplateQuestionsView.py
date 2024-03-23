from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models.AnswerTemplateQuestions import AnswerTemplateQuestions
from ..models.Questions import Questions
from ..serializers.QuestionsSerializer import QuestionsSerializer
from django.db.models import Max
from django.db.models import Max, Case, When, Exists, OuterRef
from django.db.models import Max, OuterRef, Subquery
from rest_framework.request import Request



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
# def get_template_questions(request):
#     user = request.user

#     # Get the maximum page among active questions
#     max_page = Questions.objects.filter(active=True).aggregate(max_page=Max('page'))['max_page']
    
#     # Get all template questions
#     template_questions = Questions.objects.filter(active=True).order_by('order')

#     # Serialize the template questions
#     serializer = QuestionsSerializer(template_questions, many=True)

#     # Get user's answers for the template questions
#     user_answers = {}
#     for question in template_questions:
#         try:
#             answer = AnswerTemplateQuestions.objects.get(user=user, question=question)
#             user_answers[question.id] = answer.answer_text
#         except AnswerTemplateQuestions.DoesNotExist:
#             pass

#     # Return the template questions along with user's answers
#     return Response({'max_page': max_page, 'questions': serializer.data, 'user_answers': user_answers})

def get_template_questions(request):
    user = request.user

    # Get the maximum page among active questions
    max_page = Questions.objects.filter(active=True).aggregate(max_page=Max('page'))['max_page']
    
    # Get all template questions with user's answers
    template_questions = Questions.objects.filter(active=True).order_by('order')

    # Pass the request object to the serializer context
    serializer = QuestionsSerializer(template_questions, many=True, context={'request': request})

    return Response({'max_page': max_page, 'questions': serializer.data })



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_template_pages(request):
    # Get the maximum page among active questions
    max_page = Questions.objects.filter(active=True).aggregate(max_page=Max('page'))['max_page']
    
    # Return the maximum page value in the response
    return Response({'max_page': max_page})