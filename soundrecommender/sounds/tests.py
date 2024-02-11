from django.test import TestCase

# Create your tests here.
import json

from django.test import TestCase, Client
from sounds.models import Sound


# Create your tests here.
class SoundTests(TestCase):

    def setUp(self):
        self.c = Client()


    def test_create_sounds(self):
        data = {'data': [{"title": "test song", "bpm": 120, "genres": ["pop"], "duration_in_seconds": 120,
                          "credits": [ {"name": "test person", "role": "VOCALIST"},
                                       {"name": "Ooyy", "role": "PRODUCER" }]
        }]}
        response = self.c.post("/admin/sounds", json.dumps(data), content_type="application/json")
        assert response.status_code == 201, response.status_code
        data_with_id = data.copy()
        data_with_id['data'][0]['id'] = int(Sound.objects.first().pk)
        assert json.loads(response.content) == data_with_id, json.loads(response.content)

    def test_get_all_sounds(self):
        test_sound = Sound.objects.create(title='Test Sound',
                             bpm=80,
                             duration_in_seconds=320,
                             genres=json.dumps([]),
                             credits=json.dumps([]))
        response = self.c.get("/sounds")
        assert response.status_code == 200
        assert json.loads(response.content) == {'data': [test_sound.to_dict()]}

