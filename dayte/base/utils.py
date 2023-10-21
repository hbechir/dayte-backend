from django.contrib.auth.models import User
from .models import Profile, DailySuggestion

import random

def getSuggestions(user, profile):
    """gets a list of profiles to display on the home page"""
    #check if the user can load the home screen
    if not profile.should_load_home_screen():
        daily_suggestion = DailySuggestion.objects.get(user=user)
        suggested_users = daily_suggestion.suggestions.all()
        return suggested_users
        
    # Get all profiles that have at least one interest in common with the given profile and are not staff users
    common_profiles = Profile.objects.filter(interests__in=profile.interests.all()).exclude(user=user).exclude(gender=profile.gender).exclude(user__is_staff=True)
    # Sort the common profiles by the number of common interests
    common_profiles = sorted(common_profiles, key=lambda p: p.interests.filter(pk__in=profile.interests.all()).count(), reverse=True)

    # Get the number of profiles to display daily based on the user's plan
    grid = userPlanGrid(user)

    # If there are not enough common profiles, get more profiles without interest limitation
    if len(common_profiles) < grid:
        remaining_profiles = Profile.objects.exclude(user=user).exclude(gender=profile.gender).exclude(pk__in=[p.pk for p in common_profiles]).exclude(user__is_staff=True)
        common_profiles = list(common_profiles) + random.sample(list(remaining_profiles), min(len(remaining_profiles), grid - len(common_profiles)))

    # Shuffle the profiles and return a list of users
    common_profiles = random.sample(common_profiles, min(len(common_profiles), grid))
    suggested_users = User.objects.filter(profile__in=common_profiles)
    daily_suggestion = DailySuggestion.objects.create(user=user)
    daily_suggestion.suggestions.set(suggested_users)
    daily_suggestion.save()
    profile.set_last_home_screen_load()

    return list(suggested_users)


def userPlanGrid(user):
    """ returns the number of profiles to display daily based on the user's plan """
    if user.profile.plan == 'free':
        return 2
    elif user.profile.plan == 'basic':
        return 9
    elif user.profile.plan == 'premium':
        return 12
    else:
        return 2