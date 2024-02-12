from collections import defaultdict

from django.http import JsonResponse
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from playlists.exceptions import NotFoundSoundId, JsonParsingError

from playlists.models import Playlist
from playlists.scoring import Score
from sounds.models import Sound
from utils.json_parser import get_data_from_request_body


@require_http_methods(["GET"])
def get_playlist(request: HttpRequest, playlist_id: int):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    return JsonResponse(data=playlist.to_dict(), status=200)


@csrf_exempt
@require_http_methods(["POST"])
def create_playlist(request: HttpRequest):
    # TODO: handle bad json format
    created_objs = []
    try:
        data = get_data_from_request_body(request)
        for item in data:
            sound_ids = [int(s_id) for s_id in item["sounds"]]
            Playlist.validate_sounds(sound_ids)
            playlist = Playlist.objects.create(title=item["title"])
            playlist.sounds.add(*list(map(lambda s: int(s), item["sounds"])))
            created_objs.append(playlist)
        return JsonResponse(
            data={"data": [obj.to_dict() for obj in created_objs]}, status=201
        )
    except (NotFoundSoundId, JsonParsingError) as e:
        return JsonResponse(data={"error": str(e)}, status=400)


@require_http_methods(["GET"])
def get_recommendation(request: HttpRequest):
    playlist = get_object_or_404(Playlist, pk=request.GET.get("playlistId"))
    playlist_sounds_pks = {s.pk for s in playlist.sounds.all()}
    all_sounds = Sound.objects.all()
    score_by_sound_id = defaultdict(int)
    for sound in all_sounds:
        if sound.pk not in playlist_sounds_pks:
            score_by_sound_id[sound.pk] = Score.get_sound_score_against_playlist(
                playlist, sound
            )

    highest_scored_sounds = sorted(
        [(sound_id, score) for sound_id, score in score_by_sound_id.items()],
        key=lambda x: x[1],
        reverse=True,
    )
    # TODO: add randomness here
    sound = (
        [Sound.objects.get(pk=[pk for pk, _ in highest_scored_sounds][0]).to_dict()]
        if len(highest_scored_sounds) > 0
        else []
    )
    return JsonResponse(data={"data": sound}, status=200)
