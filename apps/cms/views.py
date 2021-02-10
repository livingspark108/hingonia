from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DeleteView

from apps.cms.models import Page
from application.custom_classes import AdminRequiredMixin, AjayDatatableView


class CreatePageView(AdminRequiredMixin, SuccessMessageMixin, CreateView):

    model = Page
    fields = ['title', 'slug', 'content']
    template_name = 'cms/form.html'
    success_message = "%(title)s has been created successfully"
    success_url = reverse_lazy('page-list')


class ListPagesView(AdminRequiredMixin, TemplateView):
    model = Page
    template_name = 'cms/list.html'


class ListPagesViewJson(AjayDatatableView):
    model = Page
    columns = ['title', 'slug', 'actions']
    exclude_from_search_cloumn = ['actions']

    def render_column(self, row, column):
        if column == 'actions':
            edit_action = '<a href={} role="button" class="btn btn-warning btn-sm mr-1">Edit</a>'.format(
                reverse('page-edit', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-sm" data-url={} role="button">Delete</a>'.format(
                reverse('page-delete', kwargs={'pk': row.pk}))
            return edit_action + delete_action
        else:
            return super(ListPagesViewJson, self).render_column(row, column)


class UpdatePageView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Page
    fields = ['title', 'slug', 'content']
    template_name = 'cms/form.html'
    success_message = "%(title)s has been updated successfully"
    success_url = reverse_lazy('page-list')

    def get_context_data(self, **kwargs):
        context = super(UpdatePageView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


class DeletePageView(AdminRequiredMixin, DeleteView):
    model = Page

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)



