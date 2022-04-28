# Create your tasks here
# from demoapp.models import Widget

import requests
import uuid # ranodm name gen

from django.conf import settings

from celery import shared_task

CAT_URL = 'https://cataas.com/cat' # random cat generator url
# CAT_URL = "http://thecatapi.com/api/images/get?format=src&type=gif"

@shared_task
def download_cat():
    response = requests.get(CAT_URL)
    print(response.headers.get)
    print('-'*30)
    file_ext = response.headers.get('Content-Type').split('/')[1] # расширение файла берём из хедера
    file_name = settings.BASE_DIR/'cats'/(str(uuid.uuid4())+'.'+file_ext)
    with open(file_name, 'wb') as file:
        # открываем файл в режиме 'wb'(запись в байтах) w == перезапись/создание если нету
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)
    return True


