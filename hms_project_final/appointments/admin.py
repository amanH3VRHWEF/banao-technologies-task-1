from django.contrib import admin
from .models import User, Slot, Booking

# This allows you to edit these models in the /admin dashboard
admin.site.register(User)
admin.site.register(Slot)
admin.site.register(Booking)