from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import os
from dotenv import load_dotenv
import base64
from io import BytesIO
from django.core.files.base import ContentFile



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
from datetime import datetime, timedelta

from django.utils import timezone

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
    birth_date = models.DateField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, null=True, blank=True, default='free')
    gender = models.CharField(max_length=20, null=True, blank=True)
    interests = models.ManyToManyField(interests, blank=True)
    finished = models.BooleanField(choices=FINISHED_CHOICES, default=False)
    last_home_screen_load = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def should_load_home_screen(self):
        if not self.last_home_screen_load:
            return True
        else:
            return timezone.now() - self.last_home_screen_load > timedelta(hours=24)
    def set_last_home_screen_load(self):
        self.last_home_screen_load = timezone.now()
        self.save()

class DailySuggestion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='suggested')
    date = models.DateField(auto_now_add=True)
    suggestions = models.ManyToManyField(User, related_name='suggestions_for')

    def __str__(self):
        return f"{self.user.username}'s daily suggestions"


class Photo(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos')
    profile_picture = models.BooleanField(default=False)
    def str(self):
        return self.image.name
    def save_picture_from_base64(self, base64_image):
        # Decode the base64 string into binary data
        image_data = base64.b64decode(base64_image)

        # Create a ContentFile from the binary data
        image_content = ContentFile(image_data, name='picture.jpg')  # Provide a proper filename

        # Assign the ContentFile to the picture field
        self.image.save('picture.jpg', image_content, save=True)



class prompt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    def __str__(self):
        return self.prompt


class matches(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    matched = models.BooleanField(default=False)
    date_matched = models.DateTimeField(default=timezone.now)
    seen = models.BooleanField(default=False)
    user1_pref_days = models.CharField(max_length=100, default='', blank=True)
    user2_pref_days = models.CharField(max_length=100, default='', blank=True)
    def __str__(self):
        return self.user1.first_name + ' liked ' + self.user2.first_name +" and matched: "+str(self.matched)


class dayte(models.Model):
    date = models.DateTimeField(default=timezone.now)
    match = models.ForeignKey('matches', on_delete=models.SET_NULL, null=True, related_name='dayte')

    def __str__(self):
        return "Date on: "+str(self.date)

    def calc_mid(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        user1_pref_days = set(self.match.user1_pref_days.split(','))
        user2_pref_days = set(self.match.user2_pref_days.split(','))

        common_days = user1_pref_days & user2_pref_days
        if not common_days:
            return

        common_days_indices = sorted(days.index(day) for day in common_days)
        today_index = datetime.today().weekday()

        for day_index in common_days_indices:
            if day_index >= today_index:
                break
        else:
            day_index = common_days_indices[0]
        self.date = datetime.today() + timedelta((day_index - today_index) % 7)
        self.save()
        return self.date
