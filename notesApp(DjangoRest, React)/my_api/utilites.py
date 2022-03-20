from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer


def get_Notes_List(request):
    notes = Note.objects.all().order_by('-updated_at')
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


def get_Note_Detail(request, note_id):
    notes = Note.objects.get(id=note_id)
    serializer = NoteSerializer(notes, many=False)
    return Response(serializer.data)


def create_Note(request):
    data = request.data
    note = Note.objects.create(
        body=data['body']
    )
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)

def update_Note(request, note_id):
    data = request.data
    note = Note.objects.get(id=note_id)
    serializer = NoteSerializer(instance=note, data=data)

    if serializer.is_valid():
        serializer.save()

    return serializer.data


def delete_Note(request, note_id):
    note = Note.objects.get(id=note_id)
    note.delete()
    return Response('Note was deleted!')