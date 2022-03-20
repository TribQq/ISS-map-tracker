from django.urls import path
from .views import *

urlpatterns = [

    path('', get_Routes, name='get_Routes'),
    path('notes/', get_Notes, name='getNotes'),
    path('note/<str:note_id>/', get_Note, name='get_note'),
    
]