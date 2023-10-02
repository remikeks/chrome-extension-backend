from django.shortcuts import render
from django.views import View
from .models import RecordedVideo
from .tasks import transcribe_video_chunk
from django.http import JsonResponse


class UploadVideoView(View):
    def post(self, request):
        video_chunk = request.FILES['video_chunk'] # This assumes compatibility with 
        video_id = request.POST.get('video_id') # name fields on frontend

        try:
            received_video = RecordedVideo.objects.get(id=video_id)
        except RecordedVideo.DoesNotExist:
            received_video = RecordedVideo(id_field=video_id, video_file=video_chunk)

        # Save the chunk to a temporary location
        chunk_path = received_video.video_file.path + '.temp'
        with open(chunk_path, 'ab') as video_file:
            for chunk in video_chunk.chunks():
                video_file.write(chunk)

        # The is_last_chunk() method has not been implemented
        # My FE partner has been unresponsive.
        # I would need a mechanism for determining the final chunk being sent from the FE before 
        # I can concatenate the entire video
        if received_video.is_last_chunk():
            transcribe_video_chunk.delay(received_video.id, chunk_path)

            # Generate the URL for the saved video
            video_url = received_video.video_file.url

            return render(request, 'api/index.html', {'video_url': video_url})

        else:
            # If not the last chunk, save the chunk path for later concatenation
            received_video.chunk_paths.append(chunk_path)
            received_video.save()

        return JsonResponse({'message': 'Video chunk uploaded successfully'})
