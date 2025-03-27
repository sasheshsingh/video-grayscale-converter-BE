import os
import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import StreamingHttpResponse
from django.conf import settings

class ProcessVideoAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # if "video" not in request.FILES:
        #     return Response({"error": "No video file provided"}, status=400)
        # return Response(status=200)
        video_file = request.FILES["file"]
        input_video_path = os.path.join(settings.MEDIA_ROOT, "uploads", video_file.name)

        os.makedirs(os.path.dirname(input_video_path), exist_ok=True)

        with open(input_video_path, "wb+") as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)

        def generate():
            command = [
                "ffmpeg", "-i", input_video_path,
                "-vf", "format=gray,"
                       "drawtext=text='Sample Text added on Processed Video':"
                       "fontcolor=white:fontsize=30:"
                       "x=(w-text_w)/2:y=(h-text_h)/2",  # Center text
                "-c:v", "libx264", "-preset", "ultrafast", "-f", "mp4",
                "-movflags", "frag_keyframe+empty_moov", "pipe:1"
            ]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            while True:
                chunk = process.stdout.read(4096)
                if not chunk:
                    break
                yield chunk

        return StreamingHttpResponse(generate(), content_type="video/mp4")
