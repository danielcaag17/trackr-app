from django.shortcuts import get_object_or_404, render
from api.models import Video


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
    return render(request, 'detect_video.html', {
        'video': video,
        'result': "result",  # result is the entity of the video detected
        'error': None
    })


def detect_video_error(request):
    error = request.GET.get('error', 'Ha ocurrido un error desconocido.')
    code = request.GET.get('code', '500')
    return render(request, 'detect_video_error.html', {
        'video': None,
        'result': None,
        'error': error,
        'code': code
    })
