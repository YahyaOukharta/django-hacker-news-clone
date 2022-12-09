from django.contrib import admin

# Register your models here.
from .models import Story, Vote

admin.site.register([Story, Vote])