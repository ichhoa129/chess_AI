from asyncio.log import logger
import chess
import lichess.api
from time import sleep
import requests

import sys
sys.path.append('C:/project/chess_AI/chessAi/')
from myapp.services.game import Game


class LichessElo():
    def __init__(self):
        self.token = 'lip_Hx9Q2E8bwiGSYSMqIwbV'
        self.params = {'auth': self.token}

    def get_game_info(self):
        """
        Get the info of a game
        """
        game = lichess.api._api_get(
                f'/api/account/playing',
                self.params.copy(),
            )
        if game_now_play := game.get('nowPlaying'):
            return game_now_play[-1]
        return None

    def move(self, game_id, move):
        """
        Move a piece
        """
        try:
            return lichess.api._api_post(
                f'/api/board/game/{game_id}/move/{move}',
                self.params.copy(), 
                {'move': move}
            )
        except Exception as e:
            print(e)


def main():
    lichess = LichessElo()
    # game = Game()
    # game.start()
    fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    game_id = '3KiV8n8P'
    botFen = fen
    while True:
        lichess_game = lichess.get_game_info()
        sleep(1)
        if not lichess_game.get('isMyTurn'):
            sleep(2)
            lichess_game = lichess.get_game_info()
        lastMove = lichess_game.get('lastMove')
        # my_bot_color = lichess_game.get('color') # white or black
        logger.debug('lastMove: ', lastMove)
        # board = chess.Board(fen)
        url = 'https://pbl.howtoquamon.tk/api/move'
        data = {
            "move": {
                "from": lastMove[:2],
                "to": lastMove[2:4]
            },
            "fen": botFen
        }
        print('lichess: ', data)
        x = requests.post(url, json = data)
        res = x.json()
        botFen = res.get('fen')
        uci_move = res.get('move').get('from') + res.get('move').get('to')
        print('my_bot: ', uci_move)
        lichess.move(game_id, uci_move)
        # fen = board.fen()
        # logger.debug('board', fen)


def main2():
    game = Game()
    game.start()
    # Lychess go first
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    lastMove = 'e2e4'

    a = game.move2(board, {
        'from': lastMove[:2],
        'to': lastMove[2:4],
        'promotion': 'q',
        'flags': 'n', 
        'color': 'b', 
        'piece': 'p'
    })
    print('a: ', a)

if __name__ == '__main__':
    main()
    # main2()
    