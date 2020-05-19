from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


def make_messages(request):
    messages.add_message(request, messages.INFO, 'Info message')
    messages.add_message(request, messages.ERROR, 'Error message')
    messages.add_message(request, messages.WARNING, 'Warning message')
    messages.add_message(request, messages.SUCCESS, 'Success message')

    return HttpResponseRedirect(reverse('admin:index'))
