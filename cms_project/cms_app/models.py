from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile=models.CharField(max_length=12)
    address=models.CharField(max_length=50)
    def __str__(self):
        return self.username
 
class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def is_accessible_by(self, user):
        if self.is_public or self.owner == user:
            return True
        return False

    def get_like_count(self):
        return self.like_set.count()


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)