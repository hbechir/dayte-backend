from .models import Photo
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Profile, matches, prompt,dayte
from django.contrib.auth.models import User
from .utils import getSuggestions,get_unseen_matches,get_all_matches
from django.utils import timezone
import json
# Create your views here.

@api_view(['patch'])
@permission_classes([IsAuthenticated])
def update_location(request):
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
    data=[]
    for suggestion in suggestions:
        #id of the suggestion
        id = suggestion.id
        #get the name of the suggestion
        name = suggestion.first_name

        # create a dictionary for each suggestion
        suggestion_dict = {}
        # get pictures in a list with the profile picture the first one
        pictures=[]
        for photo in suggestion.profile.photo_set.all():
            pictures.append(photo.image.url)
        suggestion_dict['pictures'] = pictures
        # get list of interests
        interests=[]
        for interest in suggestion.profile.interests.all():
            interests.append(interest.name)
        suggestion_dict['interests'] = interests
        # get age from birth date
        age=None
        if suggestion.profile.birth_date:
            age=timezone.now().year-suggestion.profile.birth_date.year
        suggestion_dict['age'] = age
        # get prompts from the class prompts where the user == suggestion.user
        prompts=[]
        for p in prompt.objects.filter(user=suggestion):
            prompt_dict={}
            prompt_dict['prompt']=p.prompt
            prompt_dict['answer']=p.answer
            prompts.append(prompt_dict)
        suggestion_dict['id'] = id
        suggestion_dict['name'] = name
        suggestion_dict['prompts'] = prompts
        # get gender
        suggestion_dict['gender'] = suggestion.profile.gender
        # get location
        suggestion_dict['location'] = suggestion.profile.location
        # check if the user has liked the suggestion
        suggestion_dict['matching'] = matches.objects.filter(user1=user, user2=suggestion,matched=True).exists()
        #check if the user has liked the user
        suggestion_dict['liked'] =matches.objects.filter(user1=user, user2=suggestion,matched=False).exists()
        # append the suggestion dictionary to the data list
        data.append(suggestion_dict)


        user_dict={}
        user_dict['name']=user.first_name
        user_dict['plan'] = profile.plan
        #get the user's pictures
        pictures=[]
        for photo in profile.photo_set.all():
            pictures.append(photo.image.url)
        user_dict['pictures'] = pictures
        #get the user's interests
        interests=[]
        for interest in profile.interests.all():
            interests.append(interest.name)
        user_dict['interests'] = interests
        #get the user's prompts
        prompts=[]
        for p in prompt.objects.filter(user=user):
            prompt_dict={}
            prompt_dict['prompt']=p.prompt
            prompt_dict['answer']=p.answer
            prompts.append(prompt_dict)
        user_dict['prompts'] = prompts
        # GET THE USERS gender
        user_dict['gender']=user.profile.gender
        
    return Response({'user':user_dict,'suggestions': data,'matches':get_unseen_matches(user)}, status=status.HTTP_200_OK)
    




@api_view(['post'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
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

    #get the list of pictures  links of the user and save in an array
    pictures=[]
    for photo in profile.photo_set.all():
        pictures.append(photo.image.url)
    #get the list of pictures links of the user from the request and save in an array
    pictures_req=[]
    for photo in data.get('pictures'):
        pictures_req.append(photo)
    #check if the arrays are not the same
    if pictures!=pictures_req:
        for i in range(len(pictures_req)):
            if pictures_req[i] != pictures[i]:
                if pictures_req[i] in pictures and pictures_req[i] != pictures[i]:
                    #get the rqpic[i] in the pictures array 
                    pic=Photo.objects.get(image=pictures_req[i])
                    #change the content of the pic to the content of pictures_req[i]
                    pictures[i]=pictures_req[i]



                    pass
                pass

                


@api_view(['post'])
@permission_classes([IsAuthenticated])
def like(request):
    user=request.user
    profile=user.profile
    suggestion_id=request.data.get('id')
    suggestion=User.objects.get(id=suggestion_id)
    #check if the other user has liked me and we did not match then we alert him that they matched
    if matches.objects.filter(user1=suggestion, user2=user,matched=False).exists()  :
        match=matches.objects.get(user1=suggestion, user2=user,matched=False)
        match.matched=True
        match.save()
        #return both users profile pictures (the images field profilepicture is true)
        picture = ''
        for photo in suggestion.profile.photo_set.all():
            if photo.profile_picture:
                picture = photo.image.url
        return Response({'message': 'match','picture':picture,'id':match.id}, status=status.HTTP_200_OK)
    if matches.objects.filter(user1=user, user2=suggestion,matched=False).exists():
        print("You already liked this user")
        return Response({'message': 'You already liked this user'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        
        match=matches.objects.create(user1=user, user2=suggestion,matched=False)
        match.save()
        return Response({'message': 'You liked this user'}, status=status.HTTP_200_OK)



@api_view(['post'])
@permission_classes([IsAuthenticated])
def set_dayte_day(request):
    user=request.user
    profile=user.profile
    match_id=request.data.get('match_id')
    days_times=json.loads(request.data.get('days_times')) #a map of days and times
    days=[]
    times=[]
    for day, time in days_times.items():
        days.append(day)
        times.append(time)
    #convert the map to string
    days_str = ','.join(days)
    times_str = ','.join(times)


    match=matches.objects.get(id=match_id)
    if match.user1==user:
        match.user1_pref_days=days_str
        match.user1_pref_times=times_str
        match.seen_user1=True

    else:
        match.user2_pref_days=days_str
        match.user2_pref_times=times_str
        match.seen_user2=True

    match.save()
    #check if the other user has set their days and if so create a dayte object
    if match.user1_pref_days!='' and match.user2_pref_days!='':
        dayte_obj=dayte.objects.create(match=match)
        dayte_day = dayte_obj.calc_mid()
        dayte_obj.save()
        day_of_week = dayte_day.strftime('%A')
        date = dayte_day.strftime('%Y-%m-%d')
        time = dayte_day.strftime('%H:%M')    
        return Response({'message': 'You have a confirmed date on next '+ day_of_week + ' ' + str(date)+' at '+time}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'You have to wait for the other user to choose the date'}, status=status.HTTP_200_OK)
        

@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_all_user_matches(request):
    user=request.user
    profile=user.profile
    matches=get_all_matches(user)
    return Response({'matches':matches}, status=status.HTTP_200_OK)
