from django.db import models

class Questions(models.Model):
    TYPE_CHOICES = (
        ('text', 'Text'),
        ('area', 'Area'),
        ('bool', 'Boolean'),
        ('radio', 'Radio Botton'),
    )

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200, blank=True, null=True)
    question_text = models.CharField(max_length=255, null=False)
    AnswerId = models.CharField(max_length=255, null=True)
    QuestionId = models.CharField(max_length=255, null=True)
     
    prerequisite = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    order = models.IntegerField()
    group = models.IntegerField()
    page = models.IntegerField()

    active = models.BooleanField(default=True)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text

    def get_user_answer(self, user):
        try:
            from .AnswerTemplateQuestions import AnswerTemplateQuestions
            answer = AnswerTemplateQuestions.objects.get(user=user, question=self)
            return answer.answer_text
        except AnswerTemplateQuestions.DoesNotExist:
            return None
