from django.db import models

class CGMInput(models.Model):
    birthday = models.DateField()
    fallnumber = models.CharField(max_length=20)  # Assuming the fallnumber can have up to 20 characters
    changed_time = models.DateTimeField(auto_now=True)  # Field to store the time of last change

    def __str__(self):
        return f"CGMInput: {self.birthday} - {self.fallnumber}"
