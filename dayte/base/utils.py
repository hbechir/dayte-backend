from django.contrib.auth.models import User
from .models import Profile

import random

def getSuggestions(user, profile):
    """gets a list of profiles to display on the home page"""

    # Get all profiles that have at least one interest in common with the given profile
    common_profiles = Profile.objects.filter(interests__in=profile.interests.all()).exclude(user=user)

    grid = userPlanGrid(user)
    # Shuffle the profiles and return a list of 9 users
    opposite_gender_profiles = random.sample(list(common_profiles), min(len(common_profiles), grid))
    return User.objects.filter(profile__in=opposite_gender_profiles)


def userPlanGrid(user):
    """ returns the number of profiles to display daily based on the user's plan """
    if user.profile.plan == 'free':
        return 2
    elif user.profile.plan == 'basic':
        return 9
    elif user.profile.plan == 'premium':
        return 12
    else:
        return 0