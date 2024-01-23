import uuid
import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import AccessMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db import models
from django.http import Http404, HttpResponseRedirect

from django.contrib.auth.views import redirect_to_login
User = get_user_model()


class DateTimeModel(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
