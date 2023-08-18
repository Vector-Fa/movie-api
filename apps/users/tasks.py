from pathlib import Path

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.files import File
from django.core.files.storage import FileSystemStorage

from celery import shared_task

from .models import User


@shared_task
def send_email_task(email: str, verify_code: int):
    email = EmailMessage('verify code', f'your verify code: {verify_code}',
                         settings.EMAIL_HOST_USER, [email])
    email.send()


@shared_task
def upload_profile_image_task(image_path: str, user_id: int):
    storage = FileSystemStorage()
    image_path = Path(image_path)
    try:
        with image_path.open(mode='rb') as file:
            picture = File(file, name=image_path.name)
            user = User.objects.get(id=user_id)
            user.photo.save(image_path.name, picture)
            user.save()
    except Exception as e:
        print(e)
    finally:
        storage.delete(image_path)
