import json

from django.http import HttpResponse
from django.views import View


class ViewWrapper(View):

    view = None

    def get(self, request, *args, **kwargs):
        body, status = self.view().get(**kwargs)
        return HttpResponse(json.dumps(body), status=status, content_type='application/json')
