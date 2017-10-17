import json

from django.http import HttpResponse
from django.views import View

from .factories import SceneRepoFactory
from .serializers import SceneSerializer


class UploadScenePictureView(View):

    def post(self, request, scene_id):
        picture = request.FILES['picture']
        scene = SceneRepoFactory.create().attach_picture_to_scene(scene_id, picture)

        body = SceneSerializer.serialize(scene)
        status = 200
        return HttpResponse(json.dumps(body), status=status, content_type='application/json')
