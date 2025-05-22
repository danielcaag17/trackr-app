from ..models import Video, VideoDetectionResult, User, Tracker, MLModel, ModelMetrics
from django.shortcuts import redirect
import requests
from urllib.parse import quote
import uuid
from django.utils.timezone import now
from ..utils import generate_public_url, upload_s3, convert_url

'''
If render had more resources, fastapi_url_post would be enough, 
but since it doesn't, a get request is made which is less expensive.
'''
fastapi_url_get = 'https://trackr-ml-api.onrender.com/api/video/response'
fastapi_url_post = 'https://trackr-ml-api.onrender.com/api/video/detect'

FASTAPI_GET = True


def get_method():
    s3_url = "https://s3-us-west-2.amazonaws.com"  # An example of s3 url
    response = requests.get(fastapi_url_get)
    return s3_url, response


def post_method(video_file, video_id, user):
    s3_url = upload_s3(video_file, video_id, user)  # Save video in S3

    # Call to the API
    request_body = {
        "video_s3_url": convert_url(s3_url),
        "threshold": 0.4,
        "ml_model": "small-basic.pt"
    }
    response = requests.post(fastapi_url_post, json=request_body)
    return s3_url, response


def upload_video(request):
    if request.method == 'POST' and request.FILES['video']:
        try:
            user = User.objects.get(username="default")
            video_file = request.FILES.get('video')
            video_id = str(uuid.uuid4()).replace('-', '')  # Assign an ID to the video

            if FASTAPI_GET:
                s3_url, response = get_method()
            else:
                s3_url, response = post_method(video_file, video_id, user)

            if response.status_code != 200:
                error_msg = quote("FastAPI returned error")
                return redirect(f"/detect/error/?error={error_msg}&code=502")

            public_url = generate_public_url(video_file)
            detection_data = response.json()

            # Save data to the corresponding models
            video = Video.objects.create(
                id=video_id,
                title=video_file.name,
                autor=user,
                s3_url=s3_url,
                uploaded_at=now(),
            )

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
                public_url=public_url,
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

            # todo Eliminar video en s3 y la detección (al tanto de si se puede ver el video)

            return redirect('detect_video', video_id=video_detection_result.original_video.id)
        except Exception as e:
            error_msg = quote(str(e))  # Encode for URL
            return redirect(f"/detect/error/?error={error_msg}&code=500")

    # If it is not a valid POST
    error_msg = quote("Method not allowed or file not sent")
    return redirect(f"/detect/error/?error={error_msg}&code=400")
