from django.contrib import admin
from .models import Profile, Photo, interests, matches, DailySuggestion

# Register your models here.

admin.site.site_header = "Dayte Admin panel"

admin.site.register(Profile)
admin.site.register(Photo)
admin.site.register(interests)
admin.site.register(matches)
admin.site.register(DailySuggestion)