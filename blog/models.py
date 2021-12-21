from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils.timezone import now

class Post(models.Model):
    sno=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    author=models.CharField(max_length=14)
    slug=models.CharField(max_length=130)
    timeStamp=models.DateTimeField(blank=True)
    content=models.TextField()

    def __str__(self):
        return self.title + " by " + self.author

class Comment(models.Model):
    sno=models.AutoField(primary_key=True)
    comment_content=models.TextField(max_length=500)
    user=models.ForeignKey(User, on_delete=CASCADE)
    post=models.ForeignKey(Post, on_delete=CASCADE)
    parent_comment=models.ForeignKey('self', on_delete=CASCADE, null=True)
    timeStamp=models.DateTimeField(default=now)

    def __str__(self):
        return 'Comment no: ' + str(self.sno) + ' By ' + self.user.username + ' on post: ' + self.post.title