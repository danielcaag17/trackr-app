from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid
import time

# Simulación de almacenamiento temporal (en memoria, para demo)
video_store = {}


def upload_video(request):
    if request.method == 'POST':
        video_file = request.FILES.get('video')
        video_id = str(uuid.uuid4())  # Generamos un ID único para el video

        # Simulación de procesamiento de video (en una tarea asincrónica en producción)
        video_store[video_id] = {'status': 'processing'}

        # Simulamos un "procesamiento" que toma 5 segundos
        def simulate_processing(vid):
            time.sleep(5)  # Simula procesamiento del video
            video_store[vid]['status'] = 'done'
            video_store[vid]['video_url'] = f"/media/generated/{vid}.mp4"

        # Usar threading para simular el procesamiento asincrónico
        import threading
        threading.Thread(target=simulate_processing, args=(video_id,)).start()

        return JsonResponse({'video_id': video_id})

    return JsonResponse({'error': 'Invalid method'}, status=400)


def check_status(request, video_id):
    info = video_store.get(video_id)
    if not info:
        return JsonResponse({'error': 'Not found'}, status=404)
    return JsonResponse(info)

