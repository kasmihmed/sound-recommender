import math
from collections import defaultdict

from playlists.models import Playlist
from sounds.models import Sound


class Score:

    @classmethod
    def get_genres_score(cls, sound_genres, weigths_by_genres) -> float:
        score = 0
        for genre in sound_genres:
            score += weigths_by_genres.get(genre, 0)

        return score / sum(weigths_by_genres.values())

    @classmethod
    def get_credit_score(cls, sound_credits, weigths_by_credits) -> float:
        score = 0
        for credit in sound_credits:
            score += weigths_by_credits.get((credit['name'], credit['role']), 0)

        return score / sum(weigths_by_credits.values())

    @classmethod
    def get_bpm_score(cls, song1, song2) -> float:
        return 1 if (math.abs(song1.bpm - song2.bpm) < 10) else 1 / math.abs(song1.bpm - song2.title)

    @classmethod
    def get_genres_score(cls, sound_genres: list[str], playlist_genres: list[str]) -> float:
        return len(set(sound_genres).intersection(set(playlist_genres))) / len(playlist_genres)

    @classmethod
    def get_duration_score(cls, sound, playlist_min, playlist_max) -> float:
        return 1 if sound.duration_in_seconds in range(playlist_min, playlist_max) else 0


def build_playlist_genres_weights(playlist: Playlist) -> dict[str, int]:
    sounds = playlist.sounds.all()
    count_by_genres = defaultdict(int)
    for sound in sounds:
        for genre in sound.genres:
            count_by_genres[genre] += 1

    return count_by_genres


def build_credits(playlist: Playlist):
    sounds = playlist.sounds.all()
    count_by_credits = defaultdict(int)
    for sound in sounds:
        for credit in sound.credits:
            count_by_credits[(credit['name'], credit['role'])] += 1

    return count_by_credits


def build_playlist_flat_meta_with_weights(playlist):
    credits_with_weights = build_credits(playlist)
    genres_with_weights = build_playlist_genres_weights(playlist)
    sounds = playlist.sounds.all()
    titles = {sound.title for sound in sounds}
    durations = [sound.duration_in_seconds for sound in sounds]
    duration_in_seconds_range = (max(durations), min(durations))
    bpm = [sound.bpm for sound in sounds]
    return titles, duration_in_seconds_range, bpm, genres_with_weights, credits_with_weights


def get_score_against_playlist(playlist: Playlist, sound: Sound) -> float:
    titles, duration_in_seconds_range, bpm, genres_with_weights, credits_with_weights = build_playlist_flat_meta_with_weights(playlist)
    # TODO: improve this
    title_score = 1 if sound.title in titles else 0
    # TODO: double check this
    duration_score = Score.get_duration_score(sound, duration_in_seconds_range[0], duration_in_seconds_range[1])
    # TODO: update this
    bpm_score = Score.get_bpm_score(sound, playlist.sounds.all()[0])
    genres_score = Score.get_genres_score(sound.genres, genres_with_weights)
    credit_score = Score.get_credit_score(sound.credits, credits_with_weights)
    return credit_score + genres_score + bpm_score + bpm_score + duration_score + title_score / 6