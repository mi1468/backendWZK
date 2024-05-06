from rest_framework import serializers

from clinet_patient_form.models.AnswerTemplateQuestions import AnswerTemplateQuestions
from ..models.Questions import Questions

class QuestionsSerializer(serializers.ModelSerializer):
    # user_answer = serializers.SerializerMethodField()

    # class Meta:
    #     model = Questions
    #     fields = ['id', 'type', 'title', 'question_text', 'prerequisite', 'order', 'group', 'page', 'active', 'required', 'user_answer']

 
    # def get_user_answer(self, obj):
    #     # Add your implementation here to get user's answer for the question
    #     return "User's answer"  # Replace this with actual implementation

    # answer = serializers.CharField(source='get_answer', read_only=True)
    # answer = serializers.CharField(source='get_user_answer', read_only=True)
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Questions
        fields = ['id', 'type', 'title', 'question_text', 'prerequisite', 'order', 'group', 'page', 'active', 'required', 'answer']

    def get_answer(self, obj):
        user = self.context['request'].user
        return obj.get_user_answer(user)    