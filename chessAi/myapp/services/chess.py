import math
from chess import Board


class Chess:
    weights = {'p': 100, 'n': 280, 'b': 320,
               'r': 479, 'q': 929, 'k': 60000, 'k_e': 60000}

    pst_w = {
        'p': [
            [100, 100, 100, 100, 105, 100, 100, 100],
            [78, 83, 86, 73, 102, 82, 85, 90],
            [7, 29, 21, 44, 40, 31, 44, 7],
            [-17, 16, -2, 15, 14, 0, 15, -13],
            [-26, 3, 10, 9, 6, 1, 0, -23],
            [-22, 9, 5, -11, -10, -2, 3, -19],
            [-31, 8, -7, -37, -36, -14, 3, -31],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ],
        'n': [
            [-66, -53, -75, -75, -10, -55, -58, -70],
            [-3, -6, 100, -36, 4, 62, -4, -14],
            [10, 67, 1, 74, 73, 27, 62, -2],
            [24, 24, 45, 37, 33, 41, 25, 17],
            [-1, 5, 31, 21, 22, 35, 2, 0],
            [-18, 10, 13, 22, 18, 15, 11, -14],
            [-23, -15, 2, 0, 2, 0, -23, -20],
            [-74, -23, -26, -24, -19, -35, -22, -69],
        ],
        'b': [
            [-59, -78, -82, -76, -23, -107, -37, -50],
            [-11, 20, 35, -42, -39, 31, 2, -22],
            [-9, 39, -32, 41, 52, -10, 28, -14],
            [25, 17, 20, 34, 26, 25, 15, 10],
            [13, 10, 17, 23, 17, 16, 0, 7],
            [14, 25, 24, 15, 8, 25, 20, 15],
            [19, 20, 11, 6, 7, 6, 20, 16],
            [-7, 2, -15, -12, -14, -15, -10, -10],
        ],
        'r': [
            [35, 29, 33, 4, 37, 33, 56, 50],
            [55, 29, 56, 67, 55, 62, 34, 60],
            [19, 35, 28, 33, 45, 27, 25, 15],
            [0, 5, 16, 13, 18, -4, -9, -6],
            [-28, -35, -16, -21, -13, -29, -46, -30],
            [-42, -28, -42, -25, -25, -35, -26, -46],
            [-53, -38, -31, -26, -29, -43, -44, -53],
            [-30, -24, -18, 5, -2, -18, -31, -32],
        ],
        'q': [
            [6, 1, -8, -104, 69, 24, 88, 26],
            [14, 32, 60, -10, 20, 76, 57, 24],
            [-2, 43, 32, 60, 72, 63, 43, 2],
            [1, -16, 22, 17, 25, 20, -13, -6],
            [-14, -15, -2, -5, -1, -10, -20, -22],
            [-30, -6, -13, -11, -16, -11, -16, -27],
            [-36, -18, 0, -19, -15, -15, -21, -38],
            [-39, -30, -31, -13, -31, -36, -34, -42],
        ],
        'k': [
            [4, 54, 47, -99, -99, 60, 83, -62],
            [-32, 10, 55, 56, 56, 55, 10, 3],
            [-62, 12, -57, 44, -67, 28, 37, -31],
            [-55, 50, 11, -4, -19, 13, 0, -49],
            [-55, -43, -52, -28, -51, -47, -8, -50],
            [-47, -42, -43, -79, -64, -32, -29, -32],
            [-4, 3, -14, -50, -57, -18, 13, 4],
            [17, 30, -3, -14, 6, -1, 40, 18],
        ],

        # Endgame King Table
        'k_e': [
            [-50, -40, -30, -20, -20, -30, -40, -50],
            [-30, -20, -10, 0, 0, -10, -20, -30],
            [-30, -10, 20, 30, 30, 20, -10, -30],
            [-30, -10, 30, 40, 40, 30, -10, -30],
            [-30, -10, 30, 40, 40, 30, -10, -30],
            [-30, -10, 20, 30, 30, 20, -10, -30],
            [-30, -30, 0, 0, 0, 0, -30, -30],
            [-50, -30, -30, -30, -30, -30, -30, -50],
        ]
    }

    pst_b = {
        'p': pst_w['p'][::-1],
        'n': pst_w['n'][::-1],
        'b': pst_w['b'][::-1],
        'r': pst_w['r'][::-1],
        'q': pst_w['q'][::-1],
        'k': pst_w['k'][::-1],
        'k_e': pst_w['k_e'][::-1],
    }

    pst_opponent = {'w': pst_b, 'b': pst_w}
    pst_self = {'w': pst_w, 'b': pst_b}

    global_sum = 0

    def getMove(self, game: Board, move, depth, color):
        white_score = self.evaluate_board(game, move, self.global_sum, 'b')
        self.global_sum += white_score
        bestMove = self.makeBestMove(game, 'b', move, depth)
        
        game.push_uci(bestMove[0]['from'] + bestMove[0]['to'])

        return {
            'score': self.global_sum,
            'move': bestMove[0],
        }

    def getBestMove(self, game: Board, color: str,cur_sum, depth):
        return self.minimax(
            game, 
            depth, 
            -math.inf,
            math.inf,
            True,
            cur_sum,
            color
            )

    def makeBestMove(self, game: Board, color, move, depth):
        
        res = game.push_uci(move['from'] + move['to'])
        # print(res)
        # print(game.fen())
        if game.is_legal(res):
            raise Exception("Illegal move")

        if color == 'b':
            move = self.getBestMove(game, color, self.global_sum, depth)
        else:
            move = self.getBestMove(game, color, -self.global_sum, depth)
        
        
        self.global_sum += self.evaluate_board(game, move[0], self.global_sum, 'b')

        return move

  
        

    def evaluate_board(self, game: Board, move, prev_sum, color):
        if game.is_checkmate():  # game in checkmate
            # Check color if opponent is in checkmate (good for us)
            if move['color'] == color:
                return 10 ** 10
            else:  # Our king's in checkmate (bad for us)
                return -(10 ** 10)

        if game.is_stalemate() or game.can_claim_threefold_repetition() or game.is_variant_draw():  # in draw, in threefold repetition, in stalemate
            return 0

        if game.is_check():  # game in check
            # check color if opponent is in check (good for us)
            if move['color'] == color:
                prev_sum += 50
            else:  # Our king's in check (bad for us)
                prev_sum -= 50

        from_position = [8 - int(move['from'][1]),
                         ord(move['from'][0]) - ord('a')]
        to_position = [8 - int(move['to'][1]),
                       ord(move['to'][0]) - ord('a')]

        if prev_sum < -1500:
            if move['piece'] == 'k':
                move['piece'] = 'k_e'

        if 'captured' in move.keys() and move['captured'] != None:
            # check opponent piece was captured (good for us)
            if move['color'] == color:
                prev_sum += self.weights[move['captured']] + self.pst_opponent[move['color']
                                                                               ][move['captured']][to_position[0]][to_position[1]]
            # Our piece was captured (bad for us)
            else:
                prev_sum -= self.weights[move['captured']] + self.pst_self[move['color']
                                                                           ][move['captured']][to_position[0]][to_position[1]]

        if move['flags'] == 'p':
            # promote to queen
            move['promotion'] = 'q'

            if move['color'] == color:
                prev_sum -= self.weights[move['piece']] + self.pst_self[move['color']
                                                                        ][move['piece']][from_position[0]][from_position[1]]
                prev_sum += self.weights[move['promotion']] + self.pst_self[move['color']
                                                                            ][move['promotion']][to_position[0]][to_position[1]]
            else:
                prev_sum += self.weights[move['piece']] + self.pst_self[move['color']
                                                                        ][move['piece']][from_position[0]][from_position[1]]
                prev_sum -= self.weights[move['promotion']] + self.pst_self[move['color']
                                                                            ][move['promotion']][to_position[0]][to_position[1]]
        else:
            if move['color'] != color:
                prev_sum += self.pst_self[move['color']
                                          ][move['piece']][from_position[0]][from_position[1]]
                prev_sum -= self.pst_self[move['color']
                                          ][move['piece']][to_position[0]][to_position[1]]
            else:
                prev_sum -= self.pst_self[move['color']
                                          ][move['piece']][from_position[0]][from_position[1]]
                prev_sum += self.pst_self[move['color']
                                          ][move['piece']][to_position[0]][to_position[1]]

        return prev_sum

    def minimax(self, game: Board, depth, alpha, beta, is_maximizing_player, sum, color):
        # position_count += 1
        # print(game.fen())
        children = [{
            'color': 'w' if game.turn == 'white' else 'b',
            'from': move.uci()[:2],
            'to': move.uci()[2:],
            'piece': game.piece_at(move.from_square).symbol().lower(),
            'captured': game.piece_at(move.to_square).symbol().lower() if game.piece_at(move.to_square) != None else None,
            'promotion': 'q',
            'flags': 'p' if game.promoted else 'n'
        } for move in game.legal_moves]
        
        # print(children)
                
        if depth == 0 or len(children) == 0: return [None, sum]

        max_value = -math.inf
        min_value = math.inf

        # find children from g8 to f6
        
        for i in range(len(children)):
            # cloneGame = game.copy()
            # cloneGame.push_uci(children[i]['from'] + children[i]['to'])
           
            # print(children[i])
            # print(sum)
            # print(color)
            # return
            new_sum = self.evaluate_board(game, children[i], sum, color)
            # print(new_sum)
            
            [child_best_move, child_value] = self.minimax(game, depth - 1, alpha, beta, not is_maximizing_player, new_sum, color)
        
            # game.undo()
            
            if is_maximizing_player:
                if child_value > max_value:
                    max_value = child_value
                    best_move = children[i]
                    # best_move = current_pretty_move
                alpha = max(alpha, max_value)
            else:
                if child_value < min_value:
                    min_value = child_value
                    best_move = children[i]
                    # best_move = current_pretty_move
                beta = min(beta, min_value)
            
            if alpha >= beta: break
        
        return [best_move, max_value] if is_maximizing_player else [best_move, min_value]