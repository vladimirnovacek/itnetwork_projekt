from django.http import Http404
from django.views import generic

from insurance_app import models
from insurance_project import template_names as template


class ClientListView(generic.ListView):
    model = models.Person
    template_name = template.CLIENT_LIST

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        else:
            return super().get(request, *args, **kwargs)
