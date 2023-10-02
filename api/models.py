from django.contrib.postgres.fields import ArrayField
from django.db import models
import uuid


class RecordedVideo(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    video_file = models.FileField(upload_to='recorded_videos/')
    transcription = models.TextField(blank=True)
    chunk_paths = ArrayField(models.CharField(max_length=255), blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def is_last_chunk(self):
        #Not yet implemented
        pass

    def save_chunk_path(self, chunk):
        if self.chunk_paths is None:
            self.chunk_paths = []
        self.chunk_paths.append(chunk)
        self.save()
