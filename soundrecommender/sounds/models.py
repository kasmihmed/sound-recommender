from enum import Enum
from typing import TypedDict

from django.db import models


class CreditRole(str, Enum):
    VOCALIST = "VOCALIST"
    PRODUCER = "PRODUCER"


class Genre(str, Enum):
    POP = "POP"
    ROCK = "ROCK"


class Credit(TypedDict):
    name: str
    role: CreditRole


class Sound(models.Model):
    title = models.CharField(max_length=120)
    bpm = models.IntegerField()
    duration_in_seconds = models.IntegerField()
    genres = models.JSONField()
    credits = models.JSONField()

    def to_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "bpm": self.bpm,
            "duration_in_seconds": self.duration_in_seconds,
            "genres": self.genres,
            "credits": self.credits,
        }

    def flat_meta_data(self):
        flat_credits = {
            f'credit_{credit["role"]}': credit["name"] for credit in self.credits
        }
        return {
            "bpm": self.bpm,
            "title": self.title,
            "duration_in_seconds": self.duration_in_seconds,
            "genres": self.genres,
            **flat_credits,
        }

    @classmethod
    def validate_genres(cls, genres: list[str]):
        valid_genres = {g.value for g in Genre}
        non_valid_genres = set(map(lambda g: g.upper(), genres)) - valid_genres
        if len(non_valid_genres) > 0:
            formated_non_valid_genres = ", ".join(non_valid_genres)
            raise ValueError(
                f"the given genre(s) is/are not recognised: {formated_non_valid_genres}"
            )

    @classmethod
    def validate_credits(cls, credits: list[Credit]):
        valid_credit_roles = {g.value for g in CreditRole}
        non_valid_credit_roles = (
            set(map(lambda r: r.upper(), (c["role"] for c in credits)))
            - valid_credit_roles
        )
        if len(non_valid_credit_roles) > 0:
            formated_non_valid_credit_roles = ", ".join(non_valid_credit_roles)
            raise ValueError(
                f"the given credit role(s) is/are not recognised: {formated_non_valid_credit_roles}"
            )
