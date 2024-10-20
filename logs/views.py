from django.shortcuts import redirect
import os
from django.views import View
from django.shortcuts import render

from application.custom_classes import AdminRequiredMixin


class BaseLogViewerView(AdminRequiredMixin, View):
    log_directory = 'application/logs'  # Base directory for logs
    log_filename = 'errors.log'  # Default log file name

    def get_log_content(self, date=None):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Check if a specific date log file is requested
        if date:
            log_file_path = os.path.join(BASE_DIR, self.log_directory, f'{self.log_filename}.{date}')
        else:
            log_file_path = os.path.join(BASE_DIR, self.log_directory, self.log_filename)

        try:
            with open(log_file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return "Log file not found."

    def get(self, request, date=None):
        log_content = self.get_log_content(date)
        return render(request, 'log_viewer.html', {'log_content': log_content})


class ErrorLogViewerView(BaseLogViewerView):
    log_filename = 'errors.log'  # Use the errors log file


class ErrorLogViewerSingleView(ErrorLogViewerView):
    def get(self, request, date):
        return super().get(request, date=date)


class CustomLogViewerView(BaseLogViewerView):
    log_filename = 'custom.log'  # Use the custom log file


class CustomLogViewerSingleView(CustomLogViewerView):
    def get(self, request, date):
        return super().get(request, date=date)
