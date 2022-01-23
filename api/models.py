from django.db import models

# Create your models here.

class Country(models.Model):
    country = models.CharField(max_length=50)
    
class Parameter(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    parameter = models.CharField(max_length=50)