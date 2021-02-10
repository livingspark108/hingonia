from django.db import models
from django.contrib.auth import get_user_model

from application.constants import week_choice
from application.custom_model import DateTimeModel
from application.validators import image_validate_file_extension

User = get_user_model()


# Teacher Dashboard
class TeacherDashboard(DateTimeModel):
    title = models.CharField('Title ', max_length=100, blank=False, null=True)
    description = models.TextField('Description ', null=True,blank=True, help_text='Enter a description ')

    def __str__(self):
        return self.title


# Supervisor Dashboard
class SupervisorDashboard(DateTimeModel):
    title = models.CharField('Title ', max_length=100, blank=False, null=True)
    description = models.TextField('Description ', null=True,blank=True, help_text='Enter a description ')

    def __str__(self):
        return self.title


# Guide Dashboard
class GuideDashboard(DateTimeModel):
    title = models.CharField('Title ', max_length=100, blank=False, null=True)
    description = models.TextField('Description ', null=True,blank=True, help_text='Enter a description ')

    def __str__(self):
        return self.title
