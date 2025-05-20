from django.shortcuts import get_object_or_404, render
from api.models import Video, VideoDetectionResult


# Create your views here.
def home(request):
    return render(request, 'home.html')


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
