from django.db import models
from datetime import date
# Create your models here.

class Blog(models.Model):
    blog_title=models.CharField(max_length=500)
    blog_image=models.FileField()
    description = models.TextField(max_length=2000, help_text="Enter you blog text here.")
    post_date = models.DateField(default=date.today)

    def __str__(self):
        return self.blog_title
