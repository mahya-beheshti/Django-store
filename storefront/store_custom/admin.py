from django.contrib import admin
from store.admin import ProductAdmin
from tags.models import TaggedItem
from django.contrib.contenttypes import GenericTabularInline
# Register your models here.

class TagInline(GenericTabularInline):
    autoComplete_fileds =['tag']
    model = TaggedItem