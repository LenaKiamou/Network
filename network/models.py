from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="post_owner")
    description = models.CharField(max_length = 2000)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name="post_likes")

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.owner} : {self.description}"

    def total_likes(self):
        return self.liked.count() 

    def serialize(self):
        return { 
            "post_id" : self.id,
            "likes": self.total_likes(),
            "description" : self.description
            }


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ManyToManyField('Follow', null=True, blank=True, related_name="followings")

    def __str__(self):
        return f"{self.follower}"


