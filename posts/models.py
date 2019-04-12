from django.db import models

# Create your models here.
class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(blank=True)
        
    def __str__(self):
        return self.content
        

