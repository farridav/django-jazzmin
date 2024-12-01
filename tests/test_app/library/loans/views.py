from django.contrib.admin.sites import site
from django.views.generic import TemplateView


class CustomView(TemplateView):
    template_name = "loans/custom.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(site.each_context(self.request))
        return ctx
