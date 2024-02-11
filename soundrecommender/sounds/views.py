import json

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from sounds.models import Sound


# Create your views here.

@csrf_exempt
def create_sound(request: HttpRequest):
    # TODO: add some permission for admins
    if request.method == 'POST':
        errors = []
        objects_to_create = []
        # TODO: handle bad json format
        body = json.loads(request.body.decode('utf-8'))
        for item in body['data']:
            try:
                Sound.validate_genres(item['genres'])
                Sound.validate_credits(item['credits'])
                objects_to_create.append(Sound(title=item['title'],
                                     bpm=item['bpm'],
                                     duration_in_seconds=item['duration_in_seconds'],
                                     genres=item['genres'],
                                     credits=item['credits']))
            except ValueError as e:
                errors.append(e)
        if len(errors) > 0:
            return JsonResponse(data={'errors': [{'type': str(e.__class__.__name__),
                                                  'msg': str(e)} for e in errors ]}, status=400)

        Sound.objects.bulk_create(objects_to_create)
        return JsonResponse(data={'data': [obj.to_dict() for obj in objects_to_create]},status=201)

    else:
        return JsonResponse(data={'error': 'Method not allowed'}, status=405)


def get_sounds(request: HttpRequest):
    # TODO: add paginator
    sounds = Sound.objects.all()
    return JsonResponse(data={'data': [sound.to_dict() for sound in sounds]}, status=200)

