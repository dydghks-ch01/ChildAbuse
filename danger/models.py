from django.db import models

# Create your models here.
class Survey(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Manage(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)