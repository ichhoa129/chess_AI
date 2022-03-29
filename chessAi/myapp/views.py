from tokenize import String
import traceback
from django.shortcuts import render
from .services.game import Game

from rest_framework.decorators import api_view
from rest_framework.response import Response

def index(request):
    return render(request, 'index.html')

@api_view(['POST'])
def move(request):
    data = request.data
    try:
        game = Game()
        res = game.move(data['data'])
        # get machine move
        return Response({
            'status': 'success',
            'data': res
        })
    except Exception as e:
        print(traceback.format_exc())
        return Response({'error': str(e)})
    
@api_view(['POST'])
def start(request):
    data = request.data
    game = Game()
    game.depth = data['depth']
    res = game.start()
    if res:
        return Response({'status': 'ok'})
    else:
        return Response({
            'status': 'error', 
        'message': 'Game is already started'})


@api_view(['POST'])
def stop(request):
    game = Game()
    res = game.stop()
    if res:
        return Response({'status': 'ok'})
    else:
        return Response({
            'status': 'error', 
        'message': 'Game is already stopped'})
