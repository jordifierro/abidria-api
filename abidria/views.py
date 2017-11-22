import json

from django.http import HttpResponse
from django.views import View


class ViewWrapper(View):

    view_factory = None

    def get(self, request, *args, **kwargs):
        kwargs.update(request.GET.dict())
        body, status = self.view_factory.create().get(**kwargs)
        return HttpResponse(json.dumps(body), status=status, content_type='application/json')

    def post(self, request, *args, **kwargs):
        kwargs.update(request.POST.dict())
        body, status = self.view_factory.create().post(**kwargs)
        return HttpResponse(json.dumps(body), status=status, content_type='application/json')

    def patch(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8").replace("'", "\"").replace("None", "null"))
        kwargs.update(data)
        body, status = self.view_factory.create().patch(**kwargs)
        return HttpResponse(json.dumps(body), status=status, content_type='application/json')
