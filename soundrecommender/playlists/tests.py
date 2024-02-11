import json

from django.test import TestCase, Client

from playlists.models import Playlist
from sounds.models import Sound


# Create your tests here.
class PlaylistTests(TestCase):

    def setUp(self):
        self.test_sound1 = Sound.objects.create(title='Test Sound',
                             bpm=80,
                             duration_in_seconds=320,
                             genres=json.dumps([]),
                                                credits=json.dumps([]))
        self.c = Client()


    def test_create_playlist(self):
        data = {'data': [{'title': 'Test Playlist', 'sounds': [int(self.test_sound1.pk)]}]}
        response = self.c.post("/playlists", json.dumps(data), content_type="application/json")
        assert response.status_code == 201, response.status_code
        data_with_id = data.copy()
        data_with_id['data'][0]['id'] = int(Playlist.objects.first().pk)
        data_with_id['data'][0]['sounds'] = [self.test_sound1.to_dict()]
        assert json.loads(response.content) == data_with_id, json.loads(response.content)


