from celery import shared_task
from .models import RecordedVideo
import speech_recognition as sr

@shared_task
def transcribe_video(video_id):
    video = RecordedVideo.objects.get(id=video_id)
    video_path = video.video_file.path

    recognizer = sr.Recognizer()

    with sr.AudioFile(video_path) as source:
        audio = recognizer.record(source)
        try:
            transcribed_text = recognizer.recognize_google(audio)
            video.transcription = transcribed_text
            video.save()
        except sr.UnknownValueError:
            video.transcription = "Could not understand audio"
            video.save()
        except sr.RequestError:
            video.transcription = "Could not request results"
            video.save()
