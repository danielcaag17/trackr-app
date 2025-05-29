from django.shortcuts import redirect
from urllib.parse import quote
import requests
from ..utils import save_data, generate_token
from ..models import User
import uuid
from django.conf import settings

RUNNING_LOCAL = settings.RUNNING_LOCAL == "true"


def predefined_videos(request):
    if request.method == "GET":
        video_name = request.GET.get('video_id')

        if not video_name:
            error_msg = quote("Video name not sent")
            return redirect(f"/detect/error/?error={error_msg}&code=500")

        token = generate_token()
        headers = {"Authorization": f"Bearer {token}"}

        params = {
            'file_name': video_name + "_detected"
        }

        if not RUNNING_LOCAL:
            fastapi_url_get = settings.API_URL
        else:
            fastapi_url_get = 'http://127.0.0.1:5000'
        fastapi_url_get = fastapi_url_get + '/api/video/response'
        response = requests.get(fastapi_url_get, headers=headers, params=params)

        if response.status_code != 200:
            error_msg = f"Error: {response.status_code} - {response.text}"
            error_msg = quote(error_msg)
            return redirect(f"/detect/error/?error={error_msg}&code=502")

        detection_data = response.json()

        user, created = User.objects.get_or_create(
            username="default",
            defaults={"email": "default@example.com"}
        )

        video_id = str(uuid.uuid4()).replace('-', '')

        # Save data to the corresponding models
        args = {
            "video_id": video_id,
            "video_name": video_name,
            "user": user,
            "s3_url": detection_data["original_video"],
            "detection_data": detection_data,
        }
        video_detection_result = save_data(args)

        return redirect('detect_video', video_id=video_detection_result.original_video.id)

    # If it is not a valid POST
    error_msg = quote("Method not allowed")
    return redirect(f"/detect/error/?error={error_msg}&code=400")
