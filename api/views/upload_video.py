from django.http import JsonResponse
from ..models import Video, VideoDetectionResult, User
from django.shortcuts import redirect
import requests
import tempfile
from urllib.parse import quote
import uuid
from django.conf import settings
from django.utils.timezone import now
import boto3
from qtfaststart import processor


# Simulación de almacenamiento temporal (en memoria, para demo)
video_store = {}


def upload_s3(video_file, video_id, user):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    s3_file_key = f"original_videos/{video_file.name}"

    s3.upload_fileobj(
        video_file,
        settings.AWS_STORAGE_BUCKET_NAME,
        s3_file_key,
        ExtraArgs={'ContentType': 'video/mp4'}
        # 'ContentType': video_file.content_type
    )

    # Generar URL firmada (válida por 1 hora)
    public_url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': s3_file_key
        },
        ExpiresIn=3600  # 1 hora
    )

    s3_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{s3_file_key}"
    return s3_url, public_url


def upload_video(request):
    # tambien se puede hacer request.FILES.get('video'), por si falla
    if request.method == 'POST' and request.FILES['video']:
        try:
            user = User.objects.get(username="default")
            video_file = request.FILES.get('video')
            video_id = str(uuid.uuid4()).replace('-', '')
            '''''
            # Crear archivo temporal para input
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
                for chunk in video_file.chunks():
                    temp_input.write(chunk)
                temp_input_path = temp_input.name

            # Crear archivo temporal para output (con faststart)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_output:
                temp_output_path = temp_output.name

            # Aplicar faststart (moov atom al inicio)
            processor.process(temp_input_path, temp_output_path)

            # Subir el nuevo archivo a S3
            with open(temp_output_path, 'rb') as processed_file:
                class FileObj:
                    def __init__(self, file, name, content_type):
                        self.file = file
                        self.name = video_file.name
                        self.content_type = video_file.content_type

                    def read(self, *args):
                        return self.file.read(*args)

                s3_url, public_url = upload_s3(
                    FileObj(processed_file, video_file.name, video_file.content_type),
                    video_id,
                    user
                )
            '''
            # Guardar video en s3
            # Guardar modelo video
            # 1. Guardar el video en la base de datos (y subirlo al sistema de archivos/S3 si está configurado)
            s3_url, public_url = upload_s3(video_file, video_id, user)
            video = Video.objects.create(
                id=video_id,
                title=video_file.name,
                autor=user,
                s3_url=s3_url,
                public_url=public_url,
                uploaded_at=now(),
            )

            # Llamar a FastAPI
            # Guardar modelo video detected (asociado a video + persona, tiene modelo de atributo más stats)
            # 2. Llamar a FastAPI para procesar el video (usamos requests)
            fastapi_url = 'http://localhost:8001/process-video/'  # Ajusta según tu API real
            '''
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
            '''

            return redirect('detect_video', video_id=video.id)
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

