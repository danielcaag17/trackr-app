# Trackr Backend

Trackr Backend is a Django-based project that allows users to upload a video through a web interface and receive it back with bounding boxes highlighting detected people in each frame. The core functionality relies on person detection, but the architecture allows for future expansion.

The project includes two Django apps:
- `api`: Handles backend logic and communication with the external detection service.
- `web`: Manages the frontend interface using HTML, JavaScript, and CSS.

> This is a component of a final degree project. It is mostly complete and ready for usage but still open for contributions and enhancements.

---

## Live Demo

The project is deployed on [Render](https://trackr-backend-90gi.onrender.com/). Note that, due to limited resources on the free tier:
- **Video upload with live detection is only supported locally**, when connected to the companion detection API.
- **In production**, users can explore pre-processed sample videos with bounding boxes already applied.

---

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, JavaScript, CSS (inside the `web` app)
- **External Integration**: Communicates with a custom-made person detection API

---

## Getting Started

### Requirements

- Python 3.10+
- Virtual environment (recommended)
- `.env` file based on `.env.example`

### Installation

```bash
git clone https://github.com/PersonRecognition-TFG/trackr-backend.git
cd trackr-backend
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Environment Variables

You must create a `.env` file based on the `.env.example` provided. Below are the main environment variables required:

#### 🔐 Django Configuration
- **DJANGO_SECRET_KEY**: `django-secret-key`
- **DJANGO_DEBUG**: `true`
- **DEFAULT_DATABASE**:`true`
- **RUNNING_LOCAL**: `true`

#### AWS S3 Configuration
- **AWS_ACCESS_KEY_ID**: `aws_access_key`
- **AWS_SECRET_ACCESS_KEY**: `aws_secret_key`
- **AWS_STORAGE_BUCKET_NAME**:`my_bucket_name`
- **AWS_REGION**: `AWS_REGION`

#### JWT Configuration
- **JWT_SECRET**: `jwt_secret_key`
- **JWT_ALGORITHM**: `HS256`

#### External Detection API
- **API_URL**: `https://api_url.com/`

## Related Projects
- You can find the source code for the detection API in the same organization [trackr-detection-api](https://github.com/PersonRecognition-TFG/trackr-ml-api)

## JWT Security
To secure API access, the backend implements JSON Web Token (JWT)-based authentication. This allows only authenticated users to interact with the endpoints that handle video uploads and communication with the discovery service.

## Running Locally
To run the app locally with full functionality (including video detection):
1. Clone and install dependencies.
2. Start the external detection API locally.
3. Set the environment variables using the `.env` file.
4. Run the Django server:

```bash
python manage.py migrate
python manage.py runserver
```

Visit http://127.0.0.1:8000 to use the web interface.

### Features
- Upload videos and receive them back with bounding boxes on detected people 
- Explore preprocessed demo videos in production 
- Modular Django architecture (api and web apps)
- Cloud storage integration via AWS S3
- Easily configurable through environment variables

### Contributing
Contributions are welcome! Since this project started as a final degree submission, it currently has no contribution rules — feel free to fork it, open issues, or submit pull requests.

### Autor
Developed by @danielcaag17

### License
This project is licensed under the MIT License. You are free to use, copy, modify, merge, publish, distribute, and sublicense the software.



