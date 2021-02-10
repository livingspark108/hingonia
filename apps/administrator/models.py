from django.contrib.auth.models import AbstractUser
from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField


class NewsletterSubscription(models.Model):
    email = models.EmailField('Email Address', blank=False, null=False, unique=True)
    subscribed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AdminNewsletterContent(models.Model):
    title = models.CharField(max_length=50)
    newsletter_content = RichTextUploadingField(blank=True, null=True)
    publish_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_published(self):
        self.publish_count += 1
        self.save()
