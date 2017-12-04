import json

from django.http import HttpResponse
from django.views import View

from .factories import create_scene_repo
from .serializers import SceneSerializer


class UploadScenePictureView(View):

    def post(self, request, scene_id):
        picture = request.FILES['picture']
        scene = create_scene_repo().attach_picture_to_scene(scene_id, picture)

        body = SceneSerializer.serialize(scene)
        status = 200
        return HttpResponse(json.dumps(body), status=status, content_type='application/json')
