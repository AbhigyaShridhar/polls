from django.contrib import admin

from .models import User, Poll, Choice
# Register your models here.
admin.site.register(User)
admin.site.register(Choice)
admin.site.register(Poll)
