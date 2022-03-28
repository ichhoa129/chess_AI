from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

def index(request):
    return render(request, 'index.html')

@api_view(['POST'])
def move(request):
    data = request.data
    print(data)
    # get machine move
    return Response({'move': 'e4'})