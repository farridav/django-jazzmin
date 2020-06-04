from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseServerError, Http404
from django.urls import reverse


def make_messages(request):
    messages.add_message(request, messages.INFO, 'Info message')
    messages.add_message(request, messages.ERROR, 'Error message')
    messages.add_message(request, messages.WARNING, 'Warning message')
    messages.add_message(request, messages.SUCCESS, 'Success message')

    return HttpResponseRedirect(reverse('admin:index'))


def five_hundred(request):
    return HttpResponseServerError()


def four_oh_four(request):
    raise Http404('The requested admin page does not exist.')
