var express = require('express');
const { movePiece } = require('../service/move.service');
var router = express.Router();

/* GET home page. */
router.post('/api/move', function(req, res, next) {
  const {move, fen} = req.body;
  

  const {oldMove, newMove, newFen} = movePiece(move, fen);

  res.status(200).json({
    oldMove,
    move: newMove,
    fen: newFen
  })
});

module.exports = router;
