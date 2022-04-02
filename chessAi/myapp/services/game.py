from ast import Raise
from distutils import dep_util
import numpy as np
import chess

from .chess import Chess

from .SingletonMeta import SingletonMeta

class Game(metaclass=SingletonMeta):
    _instance = None
    isPlaying = False
    board = None
    current_move = None
    depth = 3

    def __init__(self):
        print("Game init")
        self.board = chess.Board()

    def start(self):
        if self.isPlaying:
            return False
        self.isPlaying = True
        return True
    
    def stop(self):
        if not self.isPlaying:
            return False
        self.isPlaying = False
        self.board.reset()
        return True
    
    def move(self, move):
        if not self.isPlaying:
            Raise(Exception("Game is not started"))
        self.current_move = move
        gameBoard = Chess()
        result = gameBoard.getMove(self.board, move, self.depth, 'b')
        return result



    