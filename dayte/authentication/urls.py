from django.contrib import admin
from django.urls import path,include
from .views import phone_number_register,phone_number_verification,finish_profile
from base.views import home

urlpatterns = [
    path('', include('drf_social_oauth2.urls', namespace='drf')),
    path('phone-number-register/', phone_number_register, name='phone-number-register'),
    path('phone-number-verification/', phone_number_verification, name='phone-number-verification'),
    # path('home/', home, name='home'),
    path('finish-profile/', finish_profile, name='finish-profile')
    

]
