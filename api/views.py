from django.shortcuts import render
from django.views import View
from .models import RecordedVideo

class UploadVideoView(View):
    def post(self, request):
        video = request.FILES['video']
        received_video = RecordedVideo(video=video)
        received_video.save()

        transcribe_video.delay(received_video.id)
        # Generate the URL for the saved video
        video_url = received_video.video.url

        return render(request, 'api/index.html', {'video_url': video_url})