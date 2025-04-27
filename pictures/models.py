from django.db import models
from django.contrib.auth.models import User
import os

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.name}-{instance.owner.id}-{instance.id}{ext}"
    return f'users/{instance.owner.username}/pictures/{final_name}'

# Create your models here.
class Picture(models.Model):
  name = models.CharField(max_length=40)
  upload_date = models.DateTimeField(auto_now_add=True)
  image = models.ImageField(upload_to='images/')
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  def __str__(self):
        return self.name