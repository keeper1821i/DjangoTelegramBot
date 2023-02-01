from django.contrib import admin
from .models import Profile
from .forms import ProfileForm


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name')
    form = ProfileForm
