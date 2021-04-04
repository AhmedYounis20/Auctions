from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(listing)
admin.site.register(comment)
admin.site.register(bid)
admin.site.register(watchlist)