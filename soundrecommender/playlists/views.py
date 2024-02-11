import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from playlists.models import Playlist


# Create your views here.
def get_playlist(request):
    return JsonResponse(content=Playlist.objects.get(pk=request.GET.get('id')).to_dict(), status=200)

@csrf_exempt
def create_playlist(request):
    # TODO: add validation
    # TODO: handle bad json format
    if request.method == 'POST':
        created_objs = []
        for item in json.loads(request.body)['data']:
            sound_ids = [int(s_id) for s_id in item['sounds']]
            Playlist.validate_sounds(sound_ids)
            playlist = Playlist.objects.create(title=item['title'])
            playlist.sounds.add(*list(map(lambda s:int(s),item['sounds'])))
            created_objs.append(playlist)
        return JsonResponse(data={'data': [obj.to_dict() for obj in created_objs]}, status=201)