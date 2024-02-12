from django.db import models
from playlists.exceptions import NotFoundSoundId

from sounds.models import Sound


# Create your models here.


class Playlist(models.Model):
    title = models.CharField(max_length=120)
    sounds = models.ManyToManyField(Sound)

    def to_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "sounds": [sound.to_dict() for sound in self.sounds.all()],
        }

    @classmethod
    def validate_sounds(cls, sound_ids: list[int]):
        existing_sounds = Sound.objects.filter(pk__in=sound_ids).values_list(
            "pk", flat=True
        )
        if set(existing_sounds) != set(sound_ids):
            missing_ids = ",".join(map(str, set(sound_ids) - set(existing_sounds)))
            raise NotFoundSoundId(
                f"the following sound id(s) do not exist: {missing_ids}"
            )
