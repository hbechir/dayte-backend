from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class interests(models.Model):
    INTEREST_CHOICES = (
        ('travelling', 'Travelling'),
        ('music', 'Music'),
        ('sports', 'Sports'),
        ('reading', 'Reading'),
        ('movies', 'Movies'),
        ('cooking', 'Cooking'),
        ('gaming', 'Gaming'),
        ('photography', 'Photography'),
        ('dancing', 'Dancing'),
        ('painting', 'Painting'),
        ('gardening', 'Gardening'),
        ('writing', 'Writing'),
        ('fishing', 'Fishing'),
        ('shopping', 'Shopping'),
        ('hiking', 'Hiking'),
        ('camping', 'Camping'),
        ('running', 'Running'),
        ('swimming', 'Swimming'),
        ('cycling', 'Cycling'),
        ('yoga', 'Yoga'),
        ('meditation', 'Meditation'),
        ('singing', 'Singing'),
        ('acting', 'Acting'),
        ('learning', 'Learning'),
        ('volunteering', 'Volunteering'),
        ('socializing', 'Socializing'),
        ('eating', 'Eating'),
        ('drinking', 'Drinking'),
        ('sleeping', 'Sleeping'),
        ('partying', 'Partying'),
        ('clubbing', 'Clubbing'),
        ('gambling', 'Gambling'),
        ('working', 'Working'), 
        ('studying', 'Studying'),
    )
    name = models.CharField(max_length=100, null=True, blank=True, choices=INTEREST_CHOICES)
    
    def __str__(self):
        return self.name
class Profile(models.Model):

    FINISHED_CHOICES = (
        (False, 'Incomplete'),
        (True, 'Complete'),
    )
    PLAN_CHOICES = (
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    birth_date = models.DateField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, null=True, blank=True) 
    gender = models.CharField(max_length=20, null=True, blank=True)
    interests = models.ManyToManyField(interests, blank=True)
    bio = models.TextField(null=True, blank=True)
    prompts = models.TextField(null=True, blank=True)
    finished = models.BooleanField(choices=FINISHED_CHOICES, default=False)
    def __str__(self):
        return self.user.username


class Photo(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos')
    def __str__(self):
        return self.image.name



class matches(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    matched = models.BooleanField(default=False)
    date_matched = models.DateTimeField(default=timezone.now)
    disliked = models.BooleanField(default=False)
    def __str__(self):
        return self.user1.first_name + ' - ' + self.user2.first_name