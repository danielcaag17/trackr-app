from ..models import User
from django.shortcuts import redirect
import requests
from urllib.parse import quote
import uuid
from ..utils import *
from django.conf import settings

RUNNING_LOCAL = settings.RUNNING_LOCAL


def post_method(video_file, video_id, user):
    s3_url = upload_s3(video_file, video_id, user)  # Save video in S3

    # Call to the API
    token = generate_token()
    headers = {"Authorization": f"Bearer {token}"}

    try:
        request_body = {
            "video_s3_url": convert_url(s3_url),
            "threshold": 0.4,
            "ml_model": "nano-G.pt"
        }
    except Exception as e:
        raise ValueError(f"The URL is not a valid S3 bucket. Original error: {e}")

    if RUNNING_LOCAL:
        fastapi_url_post = 'http://127.0.0.1:5000/'
    else:
        fastapi_url_post = settings.API_URL
    fastapi_url_post += 'api/video/detect'
    response = requests.post(fastapi_url_post, headers=headers, json=request_body)
    return s3_url, response


def upload_video(request):
    if request.method == 'POST' and request.FILES['video']:
        try:
            user, created = User.objects.get_or_create(
                username="default",
                defaults={"email": "default@example.com"}
            )
            video_file = request.FILES.get('video')
            video_id = str(uuid.uuid4()).replace('-', '')  # Assign an ID to the video

            try:
                s3_url, response = post_method(video_file, video_id, user)
            except Exception as e:
                error_msg = quote(str(e))
                return redirect(f"/detect/error/?error={error_msg}&code=502")

            if response.status_code != 200:
                error_msg = f"Error: {response.status_code} - {response.text}"
                error_msg = quote(error_msg)
                return redirect(f"/detect/error/?error={error_msg}&code=502")

            detection_data = response.json()

            # Save data to the corresponding models
            args = {
                "video_id": video_id,
                "video_name": video_file.name,
                "user": user,
                "s3_url": s3_url,
                "detection_data": detection_data,
            }
            video_detection_result = save_data(args)

            return redirect('detect_video', video_id=video_detection_result.original_video.id)
        except Exception as e:
            error_msg = quote(str(e))  # Encode for URL
            return redirect(f"/detect/error/?error={error_msg}&code=500")

    # If it is not a valid POST
    error_msg = quote("Method not allowed or file not sent")
    return redirect(f"/detect/error/?error={error_msg}&code=400")
