from django.db import models

# Create your models here.
class News(models.Model):
    idid = models.CharField(max_length=150)
    what = models.TextField(blank=True)
    who = models.DateTimeField(auto_now_add=True)
    when = models.DateTimeField(auto_now=True)
    where = models.TextField(blank=True)
