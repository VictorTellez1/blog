from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200,default="Test")
    author=models.ForeignKey(
        'auth.User', #. The reference is to the built-in User model
        on_delete=models.CASCADE,
        default="Test"
    )
    body = models.TextField(default="Test")

    def __str__(self):
        return self.title