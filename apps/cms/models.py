from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
from application.custom_model import DateTimeModel


class Page(DateTimeModel):
    title = models.CharField(max_length=30, blank=False)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    content = RichTextUploadingField(blank=True, null=True)
