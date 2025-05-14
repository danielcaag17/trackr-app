from django.http import JsonResponse
from ..models import Video, VideoDetectionResult
from django.shortcuts import render, redirect
import requests
from urllib.parse import quote


# Simulación de almacenamiento temporal (en memoria, para demo)
video_store = {}


def upload_video(request):
    # tambien se puede hacer request.FILES.get('video'), por si falla
    if request.method == 'POST' and request.FILES['video']:
        try:
            video_file = request.FILES.get('video')
            video_id = "0001"

            # Guardar video en s3
            # Guardar modelo video
            # 1. Guardar el video en la base de datos (y subirlo al sistema de archivos/S3 si está configurado)
            video = Video.objects.create(
                video_id=video_id,
                title=video_file.name,
                video_file=video_file
            )
            # Llamar a FastAPI
            # Guardar modelo video detected (asociado a video + persona, tiene modelo de atributo más stats)
            # 2. Llamar a FastAPI para procesar el video (usamos requests)
            fastapi_url = 'http://localhost:8001/process-video/'  # Ajusta según tu API real
            response = requests.post(fastapi_url, json={
                'video_url': request.build_absolute_uri(video.video_file.url),
                'video_id': str(video.video_id)
            })

            if response.status_code != 200:
                error_msg = quote("FastAPI devolvió error")
                return redirect(f"/detect/error/?error={error_msg}&code=502")

            detection_data = response.json()

            # Recopilar la info a mostrar en el html
            # 3. Guardar el resultado de la detección
            result = VideoDetectionResult.objects.create(
                video=video,
                person_count=detection_data.get('person_count'),
                metadata=detection_data  # o campos separados
            )
    
            # Eliminar video en s3 y la detección (todo al tanto de si se puede ver el video)
            # 4. Opcional: eliminar video físico si no quieres guardarlo
            # os.remove(video.video_file.path)  ← solo si está en disco local

            context = {
                'title': "the title video",
                'result': "the result",
                'error': None
            }
            # Renderizar con éxito
            return redirect('detect_video', video_id=video.video_id)
        except Exception as e:
            error_msg = quote(str(e))  # Codifica para URL
            return redirect(f"/detect/error/?error={error_msg}&code=500")

    # Si no es POST válido
    error_msg = quote("Método no permitido o archivo no enviado")
    return redirect(f"/detect/error/?error={error_msg}&code=400")


def check_status(request, video_id):
    info = video_store.get(video_id)
    if not info:
        return JsonResponse({'error': 'Not found'}, status=404)
    return JsonResponse(info)

