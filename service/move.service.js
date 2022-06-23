const { Chess } = require('./chess');
const {evaluateBoard, makeBestMove} = require('./game')

module.exports.movePiece = (move, fen) => {
  const game = new Chess();
  if (fen) {
    game.load(fen);
  }

  const movement = game.move({
    from: move.from,
    to: move.to,
    promotion: 'q',
  });

  if (movement === null) {
    throw new Error('Illegal move');
  }
  globalSum = evaluateBoard(game, movement, 0, 'b');

  const result = makeBestMove('b', game, globalSum);
  return {
    newMove: result.move,
    newFen: result.fen,
  };
};
