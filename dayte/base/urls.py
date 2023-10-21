from django.contrib import admin
from django.urls import path,include
from .views import home,update_location,updateProfile
from base.views import home

urlpatterns = [
    path('home/', home, name='home'),
    path('update-location/', update_location, name='phone-number-verification'),
    path('update-profile/', updateProfile, name='update-profile')
    

]