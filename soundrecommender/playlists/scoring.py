from collections import defaultdict
from dataclasses import dataclass

from playlists.models import Playlist
from sounds.models import Sound, Genre, CreditRole, Credit


@dataclass
class Range:
    min: int
    max: int

    def in_range(self, value: int) -> bool:
        return value in range(self.min, self.max + 1)


@dataclass
class Score:

    @classmethod
    def get_genres_score(cls, sound_genres: list[Genre], weights_by_genres: dict[str, int]) -> float:
        score = 0
        for genre in sound_genres:
            score += weights_by_genres.get(genre, 0)

        return score / sum(weights_by_genres.values())

    @classmethod
    def get_credit_score(cls, sound_credits: list[Credit], weights_by_credits: dict[tuple[str, str], int]) -> float:
        score = 0
        for credit in sound_credits:
            score += weights_by_credits.get((credit['name'], credit['role']), 0)

        return score / sum(weights_by_credits.values())

    @classmethod
    def get_bpm_score(cls, sound_bpm: int, playlist_bpm_range: Range) -> float:
        return 1 if sound_bpm in range(playlist_bpm_range.min, playlist_bpm_range.max+1) else 0

    @classmethod
    def get_duration_score(cls, sound: Sound, duration_range: Range) -> float:
        return 1 if sound.duration_in_seconds in range(duration_range.min, duration_range.max+1) else 0

    @classmethod
    def get_sound_score_against_playlist(cls, playlist: Playlist, sound: Sound) -> float:
        playlist_meta = PlaylistMeta.from_playlist(playlist)
        # TODO: improve this
        title_score = 1 if sound.title in playlist_meta.titles else 0
        duration_score = Score.get_duration_score(sound, playlist_meta.duration_range)
        bpm_score = Score.get_bpm_score(sound.bpm, playlist_meta.bpm_range)
        genres_score = Score.get_genres_score(sound.genres, playlist_meta.genres_with_weights)
        credit_score = Score.get_credit_score(sound.credits, playlist_meta.credits_with_weights)
        return credit_score + genres_score + bpm_score + duration_score + title_score / 6


@dataclass
class PlaylistMeta:
    titles: list[str]
    duration_range: Range
    bpm_range: Range
    genres_with_weights: dict[Genre, int]
    credits_with_weights: dict[tuple[str, CreditRole], int]

    @classmethod
    def build_credits(cls, sounds: list[Sound]):
        count_by_credits: defaultdict[tuple[str, CreditRole], int] = defaultdict(int)
        for sound in sounds:
            credits = sound.credits
            for credit in credits:
                print(credit)
                count_by_credits[(credit['name'], credit['role'])] += 1

        return count_by_credits

    @classmethod
    def build_playlist_genres_weights(cls, sounds: list[Sound]) -> dict[Genre, int]:
        count_by_genres: defaultdict[Genre, int] = defaultdict(int)
        for sound in sounds:
            for genre in sound.genres:
                count_by_genres[genre] += 1

        return count_by_genres

    @classmethod
    def from_playlist(cls, playlist: Playlist):
        sounds = list(playlist.sounds.all())
        credits_with_weights = cls.build_credits(sounds)
        genres_with_weights = cls.build_playlist_genres_weights(sounds)
        durations = [sound.duration_in_seconds for sound in sounds]
        bpms = [sound.bpm for sound in sounds]
        return cls(titles=[sound.title for sound in sounds],
                   duration_range=Range(min=min(durations), max=max(durations)),
                   bpm_range=Range(min=min(bpms), max=max(bpms)),
                   genres_with_weights=genres_with_weights,
                   credits_with_weights=credits_with_weights)