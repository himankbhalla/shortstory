from django.db import models
from Myuser.models import CustomUser
from django.utils import timezone
# Create your models here.

class HashTag(models.Model):
    name = models.CharField(max_length = 100)
    count = models.IntegerField(default = 0)
    def __str__(self):
        return '#' + self.name

shtory=0
poem=1
quote=2

TYPE_CHOICES = (
    (shtory, 'shtory'),
    (poem, 'poem'),
    (quote, 'quote'),
)
class Scribble(models.Model):
    headline=models.CharField(max_length=20 ,default='no title')
    story=models.TextField(max_length=1200)
    user=models.ForeignKey(CustomUser,related_name = 'stories_uploaded')
    on=models.DateTimeField(auto_now_add = True)
    likers= models.ManyToManyField(CustomUser, related_name = 'scribbles_liked' , blank = True)
    bookmark=models.ManyToManyField(CustomUser , related_name='scribbles_bookmarked', blank = True)
    points=models.IntegerField(default=0)
    book_points=models.IntegerField(default=0)
    reporters=models.ManyToManyField(CustomUser,related_name='stories_reported' , blank = True)
    user_tags = models.ManyToManyField(CustomUser, related_name = 'usertags_story' , blank = True)
    hash_tags = models.ManyToManyField(HashTag,related_name='hashtags_story' , blank = True)
    scribble_type=models.IntegerField(default=0 , choices=TYPE_CHOICES)
    def __str__(self):
        return self.headline
class Comment(models.Model):
    comment_by = models.ForeignKey(CustomUser, related_name='comments_posted')
    scribble = models.ForeignKey(Scribble)
    on = models.DateTimeField(auto_now_add = True)
    text = models.CharField(max_length = 100)
    def __str__(self):
        return self.text

class Report(models.Model):
    reported_by=models.ForeignKey(CustomUser,related_name='reported_story')
    scribble=models.OneToOneField(Scribble)
    on=models.DateTimeField(auto_now_add = True)
    report_reasons = (
        ('This story is a spam or a scam', 'This story is a spam or a scam'),
        ('This story puts people at risk', 'This story puts people at risk'),
        ("This story shouldn't be here ", "This story shouldn't be here"),
    )
    reason=models.CharField(max_length=30,choices=report_reasons,default='none')
    
    def __str__(self):
        return self.reason    

