from django.contrib import admin
from .models import Category, Torrent

admin.site.register(Torrent)
admin.site.register(Category)
