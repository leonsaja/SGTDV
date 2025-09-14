from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 

class Agenda(models.Model):
    user = models.CharField(verbose_name='Usuario',null=True,blank=True)
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.title