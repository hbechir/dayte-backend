from django.contrib.auth.models import User
from .models import Profile

import random

def getSuggestions(user, profile):
    # Get all profiles that have at least one interest in common with the given profile
    common_profiles = Profile.objects.filter(interests__in=profile.interests.all()).exclude(user=user)
    

    #number of common interests between the two profiles 


    # Shuffle the profiles and return a list of 9 users
    opposite_gender_profiles = random.sample(list(common_profiles), min(len(common_profiles), 9))
    return User.objects.filter(profile__in=opposite_gender_profiles)
