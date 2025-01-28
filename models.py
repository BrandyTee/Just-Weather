from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cities(models.Model):
    city_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    country = models.CharField(max_length=150)
    
    def __str__(self):
        return f"City: \t {self.name}\n Country: \t{self.country} \n"




