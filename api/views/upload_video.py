from django.http import JsonResponse
from ..models import Video, VideoDetectionResult, User, Tracker, MLModel, ModelMetrics
from django.shortcuts import redirect
import requests
import tempfile
from urllib.parse import quote
import uuid
from django.conf import settings
from django.utils.timezone import now
import boto3
from qtfaststart import processor

# Should not be this URL but because of using render I have to use ti
fastapi_url = 'https://trackr-ml-api.onrender.com/api/video/response'


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
            video_id = str(uuid.uuid4()).replace('-', '')  # Assign an ID to the video

            # s3_url, public_url = upload_s3(video_file, video_id, user)  # Save vidoe in S3
            # todo: quitar el cometnario de arriba, ahora es solo para testear
            s3_url = "https://s3-us-west-2.amazonaws.com"
            public_url = "https://s3-us-west-2.amazonaws.com"

            # Save the video
            video = Video.objects.create(
                id=video_id,
                title=video_file.name,
                autor=user,
                s3_url=s3_url,
                public_url=public_url,
                uploaded_at=now(),
            )

            # Call to the API
            response = requests.get(fastapi_url)

            if response.status_code != 200:
                error_msg = quote("FastAPI devolvió error")
                return redirect(f"/detect/error/?error={error_msg}&code=502")

            detection_data = response.json()

            # Save data to the corresponding models
            tracker_info = detection_data["metadata"]["tracker_info"]
            tracker = Tracker.objects.create(
                iou_threshold=tracker_info["iou_threshold"],
                max_age=tracker_info["max_age"],
                min_hits=tracker_info["min_hits"]
            )

            model_metrics_info = detection_data["metadata"]["model_info"]["model_metrics"]
            train_info = model_metrics_info["train"]
            val_info = model_metrics_info["validation"]
            model_metrics = ModelMetrics.objects.create(
                train_box_loss=train_info["box_loss"],
                train_cls_loss=train_info["cls_loss"],
                train_dfl_loss=train_info["dfl_loss"],
                val_box_loss=val_info["box_loss"],
                val_cls_loss=val_info["cls_loss"],
                val_dfl_loss=val_info["dfl_loss"],
                val_precision=val_info["precision"],
                val_recall=val_info["recall"],
                val_map50=val_info["mAP50"],
                val_map50_95=val_info["mAP50-95"]
            )

            model_info = detection_data["metadata"]["model_info"]
            ml_model = MLModel.objects.create(
                model_name=model_info["model_used"],
                description=model_info["model_description"],
                metrics=model_metrics
            )

            metadata = detection_data["metadata"]
            statistics = detection_data["statistics"]
            video_detection_result = VideoDetectionResult.objects.create(
                title=video_file.name,
                autor=user,
                s3_url=s3_url,
                original_video=video,
                tracker=tracker,
                ml_model=ml_model,
                frame_processed=metadata["frames_processed"],
                confidence_threshold=metadata["confidence_threshold"],
                video_duration=metadata["video_duration"],
                processing_time_seconds=metadata["processing_time_seconds"],
                video_fps=metadata["video_fps"],
                total_detections=statistics["total_detections"],
                detections_discarded=statistics["detections_discarded"],
                frames_with_detections=statistics["frames_with_detections"],
                avg_confidence=statistics["avg_confidence"],
                avg_people_per_frame=statistics["avg_people_per_frame"],
                person_presence_percent=statistics["person_presence_percent"],
                people_detected=statistics["people_detected"],
                peak_frame_id=statistics["peak_people_frame"]["frame_id"],
                peak_count=statistics["peak_people_frame"]["count"],
                detections_per_frame=statistics["detections_per_frame"],
                time_per_person=statistics["time_per_person"]
            )

            # Eliminar video en s3 y la detección (todo al tanto de si se puede ver el video)

            return redirect('detect_video', video_id=video_detection_result.original_video.id)
        except Exception as e:
            error_msg = quote(str(e))  # Codifica para URL
            return redirect(f"/detect/error/?error={error_msg}&code=500")

    # Si no es POST válido
    error_msg = quote("Método no permitido o archivo no enviado")
    return redirect(f"/detect/error/?error={error_msg}&code=400")
