import json
import urllib.parse

from django.http import HttpResponse
from django.views import View

from people.factories import create_authenticate_interactor


class ViewWrapper(View):

    view_creator_func = None
    upload_picture_name = None

    def get(self, request, *args, **kwargs):
        kwargs.update(request.GET.dict())

        logged_person_id = self.authenticate(request, **kwargs)
        kwargs.update({'logged_person_id': logged_person_id})

        body, status = self.view_creator_func(request, *args, **kwargs).get(**kwargs)
        return HttpResponse(json.dumps(body), status=status, content_type='application/json')

    def post(self, request, *args, **kwargs):
        kwargs.update(request.POST.dict())

        logged_person_id = self.authenticate(request, **kwargs)
        kwargs.update({'logged_person_id': logged_person_id})

        if self.upload_picture_name is not None:
            picture = request.FILES[self.upload_picture_name]
            kwargs.update({'picture', picture})

        body, status = self.view_creator_func(request, *args, **kwargs).post(**kwargs)
        return HttpResponse(json.dumps(body), status=status, content_type='application/json')

    def patch(self, request, *args, **kwargs):
        data = dict(urllib.parse.parse_qsl(request.body.decode("utf-8"), keep_blank_values=True))
        kwargs.update(data)

        logged_person_id = self.authenticate(request, **kwargs)
        kwargs.update({'logged_person_id': logged_person_id})

        if self.upload_picture_name is not None:
            picture = request.FILES[self.upload_picture_name]
            kwargs.update({'picture', picture})

        body, status = self.view_creator_func(request, *args, **kwargs).patch(**kwargs)
        return HttpResponse(json.dumps(body), status=status, content_type='application/json')

    def authenticate(self, request, **kwargs):
        authentication_header = request.META.get('Authorization')
        if authentication_header is None:
            return None

        access_token = authentication_header.replace('Token ', '')
        return create_authenticate_interactor().set_params(access_token=access_token).execute()
