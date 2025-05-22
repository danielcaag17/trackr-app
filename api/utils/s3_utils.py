from django.conf import settings
import boto3
import urllib.parse


# Upload the video_file to s3
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
    )

    s3_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{s3_file_key}"
    return s3_url


# With a video_file name generate its public url
def generate_public_url(video_file_name):
    # Create s3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    # Adapt the name as it is saved in s3
    name = video_file_name.split('.')[0]
    name = name + "_detected.mp4"
    s3_file_key = f"detections/{name}"

    # Generar URL firmada (válida por 1 hora)
    public_url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': s3_file_key
        },
        ExpiresIn=3600
    )
    return public_url


# Convert the S3 URL to a valid format for the FastAPI
def convert_url(s3_url):
    parsed_url = urllib.parse.urlparse(s3_url)

    # Check if the URL corresponds to an S3 bucket correctly
    if parsed_url.netloc.endswith("amazonaws.com"):
        bucket_name = parsed_url.netloc.split('.')[0]
        file_path = parsed_url.path.lstrip('/')

        s3_url = f"s3://{bucket_name}/{file_path}"
        return s3_url
    else:
        raise ValueError("The URL is not a valid S3 bucket.")
