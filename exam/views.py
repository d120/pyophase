from django.shortcuts import render
import math

from exam.models import ExamRoom
from students.models import Student

def assign(request):
    examRooms = ExamRoom.objects.filter(available=True)
    examStudents = Student.objects.filter(wantExam=True).order_by('name', 'prename')

    free_places = sum([eRoom.capacity_1_free for eRoom in examRooms])
    places_needed = len(examStudents)
    ratio = places_needed / free_places

    totalUsedPlaces = 0
    splitPoints = []

    for eRoom in examRooms:
        usedPlaces = math.ceil(eRoom.capacity_1_free * ratio)
        end = min(totalUsedPlaces + usedPlaces - 1, places_needed - 1)
        splitPoints.append(end)
        totalUsedPlaces = end + 1

    currentRoom = 0
    assignments = []
    assignmentsTmp = []
    for index, student in enumerate(examStudents):
        if index == splitPoints[currentRoom] + 1:
            assignments.append({'room':examRooms[currentRoom], 'current':len(assignmentsTmp), 'max':examRooms[currentRoom].capacity_1_free, 'students': assignmentsTmp})
            assignmentsTmp = []
            currentRoom += 1
        assignmentsTmp.append(student)

    assignments.append({'room':examRooms[currentRoom], 'current':len(assignmentsTmp), 'max':examRooms[currentRoom].capacity_1_free, 'students': assignmentsTmp})

    context = {'freePlaces':free_places, 'placesNeeded':places_needed, 'splitPoints':splitPoints, 'assignments': assignments}
    return render(request, 'exam/assign.html', context)
