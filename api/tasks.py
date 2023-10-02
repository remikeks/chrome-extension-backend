from celery import shared_task
from .models import RecordedVideo
import speech_recognition as sr

@shared_task
def transcribe_video_chunk(video_id, chunk_path):
    video = RecordedVideo.objects.get(id=video_id)

    recognizer = sr.Recognizer()

    with sr.AudioFile(chunk_path) as source:
        audio = recognizer.record(source)
        try:
            transcribed_text = recognizer.recognize_google(audio)
            video.transcription += transcribed_text
            video.save()
        except sr.UnknownValueError:
            video.transcription += "Could not understand audio\n"
            video.save()
        except sr.RequestError:
            video.transcription += "Could not request results\n"
