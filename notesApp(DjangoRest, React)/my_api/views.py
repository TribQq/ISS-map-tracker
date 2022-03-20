from urllib import response
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse


from .models import *
from .serializers import *
from .utilites import *



@api_view(['GET'])
def get_Routes(request):

    routes = [
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of notes'
        },
        {
            'Endpoint': '/notes/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        {
            'Endpoint': '/notes/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting note'
        },
    ]

    return Response(routes)


@api_view(['GET', 'POST'])
def get_Notes(request):

    if request.method == 'GET':
        return get_Notes_List(request)

    if request.method == 'POST':
        return create_Note(request)


@api_view(['GET', 'PUT', 'DELETE'])
def get_Note(request, note_id):

    if request.method == 'GET':
        return get_Note_Detail(request, note_id)

    if request.method == 'PUT':
        return update_Note(request, note_id)

    if request.method == 'DELETE':
        return delete_Note(request, note_id)


