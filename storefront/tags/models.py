from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.
class Tag(models.Model):
    labal = models.CharField(max_length=255)


class TagedItem(models.Model):
    tag = models.ForeignKey(Tag , on_delete=models.CASCADE)
    # Generic type(video , product , ...)
    content_type = models.ForeignKey(ContentType , on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_obj = GenericForeignKey()