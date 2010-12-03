from django.db import models

class WebUser(models.Model):
    name = models.CharField("name", max_length=50)
    