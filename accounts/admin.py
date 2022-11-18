from django.contrib import admin
from .models import CustomUser, Profile, Blog


admin.site.register([CustomUser, Profile, Blog])