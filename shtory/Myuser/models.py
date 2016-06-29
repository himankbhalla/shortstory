from __future__ import unicode_literals
import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('NS', '--'))
class CustomUser(AbstractUser):
    gender = models.CharField(max_length = 2, choices = GENDER_CHOICES, default = GENDER_CHOICES[2][0])
    profile_pic = models.ImageField(upload_to = 'profile_pics/', blank = True)
    dob = models.DateField(null = True, blank = True)
    phone_number = models.CharField(max_length = 12, default = '')
    following = models.ManyToManyField('self', symmetrical = False ,through ="Relationship", related_name='related_to')
    
    def image_tag(self):
        if self.profile_pic:
            return '<img height="40px" width="40px" src="/media/%s">' % self.profile_pic
        else:
            return ''
        image_tag.short_description = 'Image'
        image_tag.allow_tags = 'True'
    
    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "username__icontains")
    class Meta:
        unique_together = ('email',)

RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)

class Relationship(models.Model):
    from_person = models.ForeignKey(CustomUser, related_name='from_people')
    to_person = models.ForeignKey(CustomUser, related_name='to_people')
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)




class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())
      
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'User profiles'


class UserInfo(models.Model):
    user=models.OneToOneField(CustomUser)
    bio=models.CharField(max_length=300 , null=True)
    def __str__(self):
        return self.user.username


  