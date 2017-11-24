import json

from django.http import HttpResponse
from django.views import View

from .factories import ExperienceRepoFactory
from .serializers import ExperienceSerializer


class UploadExperiencePictureView(View):

    def post(self, request, experience_id):
        picture = request.FILES['picture']
        experience = ExperienceRepoFactory.create().attach_picture_to_experience(experience_id, picture)

        body = ExperienceSerializer.serialize(experience)
        status = 200
        return HttpResponse(json.dumps(body), status=status, content_type='application/json')
