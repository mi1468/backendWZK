from django.db import models
from django.contrib.auth.models import User  # Assuming you're using Django's built-in user model

class AnswerTemplateQuestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('Questions', on_delete=models.CASCADE)
    answer_text = models.TextField( blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s answer to {self.question.title}"
