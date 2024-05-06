from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models.AnswerTemplateQuestions import AnswerTemplateQuestions
from ..models.Questions import Questions
from ..serializers.AnswerTemplateQuestionsSerializer import AnswerTemplateQuestionsSerializer

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def submit_answer(request):
    data = request.data
    user = request.user
    answers = []

    for question_id_str, answer_text in data.items():
        try:
            question_id = int(question_id_str)
        except ValueError:
            return Response({'error': 'Invalid question_id format'}, status=400)

        try:
            question = Questions.objects.get(pk=question_id)
        except Questions.DoesNotExist:
            return Response({'error': f'Question with ID {question_id} does not exist'}, status=400)

        # Check if there is an existing answer for the user and question
        existing_answer = AnswerTemplateQuestions.objects.filter(user=user, question=question).first()

        if existing_answer:
            # Update the existing answer
            existing_answer.answer_text = answer_text
            existing_answer.save()
            answers.append(existing_answer)
        else:
            # Create a new answer instance
            answer = AnswerTemplateQuestions.objects.create(user=user, question=question, answer_text=answer_text)
            answers.append(answer)

    # Serialize the list of created/updated answers
    serializer = AnswerTemplateQuestionsSerializer(answers, many=True)
    return Response(serializer.data)