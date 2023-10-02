from django.contrib.postgres.fields import ArrayField
from django.db import models
import uuid


class RecordedVideo(models.Model):
    id_field = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    video_file = models.FileField(upload_to='recorded_videos/')
    transcription = models.TextField(blank=True)
    chunk_paths = ArrayField(models.CharField(max_length=255), blank=True, null=True)  # Add this field

    def __str__(self):
        return str(self.id_field)

    def is_last_chunk(self):
        # Assuming the last chunk is determined by some condition (e.g., a flag sent from frontend)
        # You need to implement this method based on your specific logic
        return True  # Change this to return the actual condition

    def save_chunk_path(self, chunk_path):
        # Save the chunk path to the list
        if self.chunk_paths is None:
            self.chunk_paths = []
        self.chunk_paths.append(chunk_path)
        self.save()
