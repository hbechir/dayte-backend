from django.contrib import admin
from django.urls import path,include
from .views import home,update_location,updateProfile,like,set_dayte_day,get_all_user_matches
from base.views import home

urlpatterns = [
    path('home/', home, name='home'),
    path('update-location/', update_location, name='phone-number-verification'),
    path('update-profile/', updateProfile, name='update-profile'),
    path('like/', like),
    path('set-dayte-day/', set_dayte_day),
    path('get-all-user-matches/', get_all_user_matches),

]