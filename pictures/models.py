from django.db import models

# Create your models here.
class Picture(models.Model):
  name = models.CharField(max_length=40)
  upload_date = models.DateTimeField(auto_now_add=True)
  image = models.ImageField(upload_to='images/')