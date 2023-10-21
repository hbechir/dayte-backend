from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view

from django.contrib.auth import authenticate, login
from oauth2_provider.models import AccessToken, RefreshToken

from django.contrib.auth.hashers import make_password


from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from twilio.rest import Client  # Import Twilio Client
from .serializers import PhoneNumberSerializer
from .models import Code
from base.models import Profile,Photo
from django.contrib.auth.models import User
import os
from dotenv import load_dotenv

from .utils import generate_verification_code

# Load environment variables from .env file
load_dotenv()

# Retrieve Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

# Initialize the Twilio Client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Create your views here.
@api_view(['post'])
@permission_classes([AllowAny])
def phone_number_register(request):
    #get phone number from request
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')
    password2 = request.data.get('password2')
    #check if passwords match
    if password != password2:
        return Response({'message': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
    
    user=User.objects.filter(username=phone_number)
    print(user)
    print("creating user  ..................................")
    #check if phone number is alreaady registered
    if not user or user[0].is_active==False:
        #create temporary user
        print(password)
        if not user:
            user =User.objects.create_user(username=phone_number, password=password, is_active=False)
            user.save()
            profile = Profile.objects.create(user=user,finished=False)
            profile.save()

        else:
            user=user[0]
            user.password=make_password(password)
            user.is_active=False
            user.save()
            profile=user.profile
            profile.finished=False
            profile.save()
        #generate code and store it
        generated_code = generate_verification_code()
        code = Code.objects.create(user=user,phone_number=phone_number, code=generated_code)
        code.save()



        #send code to user via sms
        message = client.messages.create(
        messaging_service_sid='MG9c70198c30b456e221c519e78c8875e7',
        body='Your verification code is :' + generated_code,
        to=phone_number
        )
    
        
        return Response({'message': 'if the number you provided is valid you will receive a verification code'}, status=status.HTTP_200_OK)
    return Response({'message': 'the provided Phone number already registered'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['post'])
@permission_classes([AllowAny])
def phone_number_verification(request):
    #get phone number and code from request
    phone_number = request.data.get('phone_number')
    code = request.data.get('code')
    #check if code is correct
    code = Code.objects.filter(phone_number=phone_number, code=code)
    if not code.exists():
        return Response({'message': 'Code expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)
    code = code.first()
    user=code.user
    user.is_active=True
    user.save()
    code.delete()

    return Response({'message': 'Phone number verified successfully, please login.'}, status=status.HTTP_200_OK)







@api_view(['POST'])
@permission_classes([IsAuthenticated])
def finish_profile(request):
    user = request.user
    data = request.data
    profile = user.profile
    #getting data
    birth_date = data.get('birth_date')
    name = data.get('name')
    birth_date = data.get('birth_date')
    gender = data.get('gender')
    interests = data.get('interests') # array of strings
    #The interests data should be in a list format.
    profile.interests.set(interests)

    #TO BE CHANGED --------------------------------------------
    bio = data.get('bio')
    prompts = data.get('prompts') # array of strings
    

    # Update profile fields
    user.first_name = name
    profile.birth_date = birth_date
    profile.gender = gender
    profile.interests = interests
    profile.bio = bio
    profile.prompts = prompts
    profile.finished = True
    profile.save()
    user.save()

    # Update photos

    #to be tested -----------------------------------------------------
    #make sure to save the pics in a folder called photos in the media folder
    photos = data.get('photos', [])
    for photo in photos:
        #mark the the first pic as the profile picture
        if photo == photos[0]:
            photo_obj = Photo.objects.create(profile=profile, image=photo, profile_picture=True)
        else:
            photo_obj = Photo.objects.create(profile=profile, image=photo,profile_picture=False)
            photo_obj.save()

    return Response({'message': 'Profile completed successfully'}, status=status.HTTP_200_OK)
