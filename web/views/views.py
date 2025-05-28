from django.shortcuts import get_object_or_404, render
from api.models import Video, VideoDetectionResult
import os
from django.conf import settings


# Create your views here.
def home(request):
    context = {
        'running_local': settings.RUNNING_LOCAL
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def legal(request):
    return render(request, 'legal.html')


def contact(request):
    return render(request, 'contact.html')


def detect_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video_detection_result = get_object_or_404(
        VideoDetectionResult,
        original_video=video,
        title=video.title,
        autor=video.autor
    )
    tracker = video_detection_result.tracker
    ml_model = video_detection_result.ml_model
    model_metrics = ml_model.metrics
    context = {
        'video': video_detection_result,
        'tracker': tracker,
        'ml_model': ml_model,
        'model_metrics': model_metrics,
        'error': None
    }
    return render(request, 'detect_video.html', context)


def detect_video_error(request):
    error = request.GET.get('error', 'Ha ocurrido un error desconocido.')
    code = request.GET.get('code', '500')
    return render(request, 'detect_video_error.html', {
        'video': None,
        'result': None,
        'error': error,
        'code': code
    })


def predefined_videos(request):
    images_dir = os.path.join(settings.STATIC_ROOT, 'predefined-videos')

    images = []
    for filename in os.listdir(images_dir):
        if filename.endswith('.jpg'):
            images.append(filename)

    return render(request, 'predefined-videos.html', {'images': images})
