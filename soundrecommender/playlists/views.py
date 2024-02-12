import json
import math
from collections import defaultdict

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from playlists.models import Playlist
from playlists.scoring import build_playlist_flat_meta_with_weights, get_score_against_playlist
from sounds.models import Sound


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




def get_recommendation(request):
    # TODO: handle not found
    playlist = Playlist.objects.get(pk=request.GET.get('playlistId'))
    sounds = playlist.sounds.all()
    # TODO: skip sounds that are already in the playlist
    all_sounds = Sound.objects.all()
    score_by_sound_id = defaultdict(int)
    for sound in all_sounds:
        score_by_sound_id[sound.pk] = get_score_against_playlist(playlist, sound)

    highest_scored_sounds = sorted([(sound_id, score) for sound_id, score in score_by_sound_id.items()], key=lambda x:x[1], reverse=True)
    # TODO: add randomness here
    sound = Sound.objects.get(pk__in=[pk for pk, _ in highest_scored_sounds][0])
    return JsonResponse(data={'data': [sound.to_dict()]}, status=200)