from rest_framework import serializers
from ..models.AnswerTemplateQuestions import AnswerTemplateQuestions

class AnswerTemplateQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerTemplateQuestions
        fields = ['id', 'user', 'question', 'answer_text']
