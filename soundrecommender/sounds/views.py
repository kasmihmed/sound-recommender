from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from playlists.exceptions import JsonParsingError
from sounds.models import Sound
from utils.json_parser import get_data_from_request_body


@csrf_exempt
@require_http_methods(["POST"])
def create_sound(request: HttpRequest):
    # TODO: add some permission for admins
    errors = []
    objects_to_create = []
    try:
        data = get_data_from_request_body(request)
        for item in data:
            try:
                Sound.validate_genres(item["genres"])
                Sound.validate_credits(item["credits"])
                objects_to_create.append(
                    Sound(
                        title=item["title"],
                        bpm=item["bpm"],
                        duration_in_seconds=item["duration_in_seconds"],
                        genres=item["genres"],
                        credits=item["credits"],
                    )
                )
            except ValueError as e:
                errors.append(e)
        if len(errors) > 0:
            return JsonResponse(
                data={
                    "errors": [
                        {"type": str(e.__class__.__name__), "msg": str(e)}
                        for e in errors
                    ]
                },
                status=400,
            )

        Sound.objects.bulk_create(objects_to_create)
        return JsonResponse(
            data={"data": [obj.to_dict() for obj in objects_to_create]}, status=201
        )
    except JsonParsingError as e:
        return JsonResponse(data={"error": str(e)}, status=400)


@require_http_methods(["GET"])
def get_sounds(request: HttpRequest):
    # TODO: add paginator
    sounds = Sound.objects.all()
    return JsonResponse(
        data={"data": [sound.to_dict() for sound in sounds]}, status=200
    )
