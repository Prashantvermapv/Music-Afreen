from django.db import models
from datetime import date
# Create your models here.

class Hots(models.Model):
    hots_title=models.CharField(max_length=500)
    hots_image=models.FileField()
    description = models.TextField(max_length=20000, help_text="Enter you blog text here.")
    post_date = models.DateField(default=date.today)

    def __str__(self):
        return self.hots_title
