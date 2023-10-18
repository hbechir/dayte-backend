from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from django.contrib.auth.models import User

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
    return Response({'message': 'Welcome to Dayte'}, status=status.HTTP_200_OK)
