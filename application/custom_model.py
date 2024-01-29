import uuid

from django.db import models
from django.db.models.query import QuerySet



class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(is_deleted=True)

    def delete_hard(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(is_deleted=False)

    def dead(self):
        return self.filter(is_deleted=True)


class SoftDeleteManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.with_deleted = kwargs.pop('deleted', None)
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.with_deleted:
            return SoftDeletionQuerySet(self.model)
        return SoftDeletionQuerySet(self.model).filter(is_deleted=False)

    def delete_hard(self):
        return self.get_queryset().delete_hard()

    def select_hard(self):
        return SoftDeletionQuerySet(self.model).filter(is_deleted=True)


class DateTimeModel(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = SoftDeleteManager()
    objects_with_deleted = SoftDeleteManager(deleted=True)

    class Meta:
        abstract = True

    def delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    def delete_hard(self):
        super(DateTimeModel, self).delete()

