import json
from django.test import TestCase, Client
from playlists.models import Playlist
from sounds.models import Sound


# Create your tests here.
class PlaylistTests(TestCase):

    def setUp(self):
        self.test_sound1 = Sound.objects.create(
            title="Test Sound", bpm=80, duration_in_seconds=320, genres=[], credits=[]
        )
        self.c = Client()

    def test_create_playlist_returns_the_playlist_back(self):
        data = {
            "data": [{"title": "Test Playlist", "sounds": [int(self.test_sound1.pk)]}]
        }
        response = self.c.post(
            "/playlists", json.dumps(data), content_type="application/json"
        )
        assert response.status_code == 201, response.status_code
        data_with_id = data.copy()
        data_with_id["data"][0]["id"] = int(Playlist.objects.first().pk)
        data_with_id["data"][0]["sounds"] = [self.test_sound1.to_dict()]
        assert json.loads(response.content) == data_with_id, json.loads(
            response.content
        )

    def test_create_a_bad_playlist_should_return_400(self):
        data = {"data": [{"title": "Test Playlist", "sounds": [-1]}]}
        response = self.c.post(
            "/playlists", json.dumps(data), content_type="application/json"
        )
        assert response.status_code == 400, response.status_code


class RecommendationTests(TestCase):
    def setUp(self):
        self.pop_sound1 = Sound.objects.create(
            title="FAST POP Sound",
            bpm=120,
            duration_in_seconds=320,
            genres=["pop"],
            credits=[{"name": "author1", "role": "PRODUCER"}],
        )

        self.pop_sound2 = Sound.objects.create(
            title="SLOW SHORT ROCK Sound",
            bpm=20,
            duration_in_seconds=20,
            genres=["rock"],
            credits=[{"name": "author1", "role": "PRODUCER"}],
        )

        self.pop_playlist1 = Playlist.objects.create(title="POP Playlist")
        self.pop_sound3 = Sound.objects.create(
            title="PLAYLIST POP Sound",
            bpm=120,
            duration_in_seconds=320,
            genres=["pop"],
            credits=[{"name": "author1", "role": "PRODUCER"}],
        )
        self.pop_playlist1.sounds.add(self.pop_sound3)
        self.c = Client()

    def test_recommendation_uses_metadata_correctly(self):
        response = self.c.get(
            "/sounds/recommended", {"playlistId": self.pop_playlist1.pk}
        )
        assert response.status_code == 200
        assert response.json() == {"data": [self.pop_sound1.to_dict()]}

    def test_recommendation_for_non_existing_playlist_returns_404(self):
        response = self.c.get("/sounds/recommended", {"playlistId": -1})
        assert response.status_code == 404, response.status_code
