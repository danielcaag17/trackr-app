from ..models import Video, VideoDetectionResult, Tracker, MLModel, ModelMetrics
from django.utils.timezone import now
from .s3_utils import generate_public_url


def save_video(video_name, video_id, user, s3_url):
    video = Video.objects.create(
        id=video_id,
        title=video_name,
        autor=user,
        s3_url=s3_url,
        uploaded_at=now(),
    )
    return video


def save_tracker(detection_data):
    tracker_info = detection_data["metadata"]["tracker_info"]
    tracker = Tracker.objects.create(
        iou_threshold=tracker_info["iou_threshold"],
        max_age=tracker_info["max_age"],
        min_hits=tracker_info["min_hits"]
    )
    return tracker


def save_model_metrics(detection_data):
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
    return model_metrics


def save_ml_model(detection_data, model_metrics):
    model_info = detection_data["metadata"]["model_info"]
    ml_model = MLModel.objects.create(
        model_name=model_info["model_used"],
        description=model_info["model_description"],
        metrics=model_metrics
    )
    return ml_model


def save_video_detection_result(detection_data, video_name, public_url, user, video, tracker, ml_model):
    metadata = detection_data["metadata"]
    statistics = detection_data["statistics"]
    video_detection_result = VideoDetectionResult.objects.create(
        title=video_name,
        autor=user,
        s3_url=detection_data["processed_video"],
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
    return video_detection_result


def save_data(args):
    video_name = args['video_name']
    video_id = args['video_id']
    user = args['user']
    s3_url = args['s3_url']
    detection_data = args['detection_data']
    public_url = generate_public_url(video_name)

    video = save_video(video_name, video_id, user, s3_url)
    tracker = save_tracker(detection_data)
    model_metrics = save_model_metrics(detection_data)
    ml_model = save_ml_model(detection_data, model_metrics)
    video_detection_result = save_video_detection_result(detection_data, video_name, public_url,
                                                         user, video, tracker, ml_model)

    return video_detection_result
