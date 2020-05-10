import datetime

from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db import models


class ArthonsysDatatableView(BaseDatatableView):
    extra_search_columns = []

    def get_filter_method(self):
        return self.FILTER_ICONTAINS

    def filter_queryset(self, qs):
        columns = self._columns
        if not self.pre_camel_case_notation:
            # get global search value
            search = self._querydict.get('search[value]', None)
            q = Q()
            filter_method = self.get_filter_method()
            for col_no, col in enumerate(self.columns_data):
                # col['data'] - https://datatables.net/reference/option/columns.data
                data_field = col['data']
                try:
                    data_field = int(data_field)
                except ValueError:
                    pass
                if isinstance(data_field, int):
                    column = columns[data_field]  # by index so we need columns definition in self._columns
                else:
                    column = data_field
                column = column.replace('.', '__')
                # apply global search to all searchable columns
                if search and col['searchable']:
                    q |= Q(**{'{0}__{1}'.format(column, filter_method): search})

                # column specific filter
                if col['search.value']:
                    qs = qs.filter(**{
                        '{0}__{1}'.format(column, filter_method): col['search.value']})

            columns = self.extra_search_columns
            for column in columns:
                column = column.replace('.', '__')
                if search:
                    search_part = search.split(' ')
                    for part in search_part:
                        q |= Q(**{'{0}__{1}'.format(column, filter_method): part})

            qs = qs.filter(q)
        return qs


class DateUserModel(models.Model):
    legacy_id = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    # def save(self,  *args, **kwargs):
    #     if self.created_at is None:
    #         self.created_at = datetime.datetime.now()
    #     if self.updated_at is None:
    #         self.updated_at = datetime.datetime.now()
    #     super(DateUserModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
