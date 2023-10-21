from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from django.contrib.auth.models import User
from .utils import getSuggestions
# Create your views here.

@api_view(['patch'])
@permission_classes([IsAuthenticated])
def update_location():
    user=request.user
    profile=user.profile
    profile.lat=request.data.get('lat')
    profile.lng=request.data.get('lng')
    #profile.location_name=request.data.get('location')
    #to be added location name---------------------------------
    profile.save()
    return Response({'message': 'Location updated'}, status=status.HTTP_200_OK)



@api_view(['get'])
@permission_classes([IsAuthenticated])
def home(request):
    user=request.user
    profile=user.profile
    if not profile.finished:
        return Response({'message': 'Please finish setting up your profile'}, status=status.HTTP_400_BAD_REQUEST)
    
    suggestions=getSuggestions(user,profile)
    #go through suggestions and make a list of profiles data to return
    suggestions=[{'id':suggestion.id,'name':suggestion.first_name,'profile_picture':suggestion.profile.photo_set.filter(profile_picture=True).first().image.url if suggestion.profile.photo_set.filter(profile_picture=True).first() else None} for suggestion in suggestions]
    return Response({'suggestions': suggestions,'plan':profile.plan}, status=status.HTTP_200_OK)

@api_view(['post'])
@permission_classes([IsAuthenticated])
def updateProfile():
    data = request.data
    user = request.user
    profile = user.profile
    if data.get('name'):
        user.name = data.get('name')
    if data.get('phone_number'):
        profile.phone_number = data.get('phone_number')
    if data.get('birth_date'):
        profile.birth_date = data.get('birth_date')
    if data.get('interests'):
        profile.interests = data.get('interests')
    if data.get('bio'):
        profile.bio = data.get('bio')
    if data.get('prompts'):
        profile.prompts = data.get('prompts')
    