var STACK_SIZE = 100; // maximum size of undo stack

var board = null;
var $board = $('#myBoard');
var game = new Chess();
var whiteSquareGrey = '#a9a9a9';
var blackSquareGrey = '#696969';

var squareClass = 'square-55d63';

var config = {
  draggable: true,
  position: 'start',
  onDragStart: onDragStart,
  onDrop: onDrop,
  onMouseoutSquare: onMouseoutSquare,
  onMouseoverSquare: onMouseoverSquare,
  onSnapEnd: onSnapEnd,
};
board = Chessboard('myBoard');

timer = null;

function checkStatus(color) {
  if (game.in_checkmate()) {
    document.getElementById("status").innerHTML = `<b>Checkmate!</b> Oops, <b>${color}</b> lost.`;
  } else if (game.insufficient_material()) {
    document.getElementById("status").innerHTML = `It's a <b>draw!</b> (Insufficient Material)`;
  } else if (game.in_threefold_repetition()) {
    document.getElementById("status").innerHTML = `It's a <b>draw!</b> (Threefold Repetition)`;
  } else if (game.in_stalemate()) {
    document.getElementById("status").innerHTML = `It's a <b>draw!</b> (Stalemate)`;
  } else if (game.in_draw()) {
    document.getElementById("status").innerHTML = `It's a <b>draw!</b> (50-move Rule)`;
  } else if (game.in_check()) {
    document.getElementById("status").innerHTML = `Oops, <b>${color}</b> is in <b>check!</b>`;
    return false;
  } else {
    document.getElementById("status").innerHTML = `No check, checkmate, or draw.`;
    return false;
  }
  return true;
}

/*
 * Resets the game to its initial state.
 */
function reset() {
  game.reset();
  $board.find('.' + squareClass).removeClass('highlight-white');
  $board.find('.' + squareClass).removeClass('highlight-black');
  $board.find('.' + squareClass).removeClass('highlight-hint');
  board.position(game.fen());
  $('#advantageColor').text('Neither side');

  // Kill the Computer vs. Computer callback
  if (timer) {
    clearTimeout(timer);
    timer = null;
  }
}

/*
 * Event listeners for various buttons.
 */
$('#ruyLopezBtn').on('click', function () {
  reset();
  game.load(
    'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 0 1'
  );
  board.position(game.fen());
  window.setTimeout(function () {
    makeBestMove('b');
  }, 250);
});
$('#italianGameBtn').on('click', function () {
  reset();
  game.load(
    'r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 0 1'
  );
  board.position(game.fen());
  window.setTimeout(function () {
    makeBestMove('b');
  }, 250);
});
$('#sicilianDefenseBtn').on('click', function () {
  reset();
  game.load('rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1');
  board.position(game.fen());
});

function ajaxStart(depth) {
  const body = {
    depth: depth,
  };
  $.ajax({
    headers: {
      'Content-Type': 'application/json',
      'Data-Type': 'json',
    },
    type: 'POST',
    url: '/api/start',
    data: JSON.stringify(body),
  });
}

function ajaxStop() {
  $.ajax({
    headers: {
      'Content-Type': 'application/json',
      'Data-Type': 'json',
    },
    type: 'POST',
    url: '/api/stop',
    data: JSON.stringify(),
    success: function (data) {
      'STOPPPPP'
      console.log(data)
      reset();
    }
  });
}

$('#startBtn').on('click', function () {
  board = Chessboard('myBoard', config);
  ajaxStart(parseInt($('#search-depth').find(':selected').text()));
});

$('#compVsCompBtn').on('click', function () {
  reset();
  compVsComp('w');
});
$('#resetBtn').on('click', function () {
  ajaxStop();
});

var undo_stack = [];

function undo() {
  var move = game.undo();
  undo_stack.push(move);

  // Maintain a maximum stack size
  if (undo_stack.length > STACK_SIZE) {
    undo_stack.shift();
  }
  board.position(game.fen());
}

$('#undoBtn').on('click', function () {
  if (game.history().length >= 2) {
    $board.find('.' + squareClass).removeClass('highlight-white');
    $board.find('.' + squareClass).removeClass('highlight-black');
    $board.find('.' + squareClass).removeClass('highlight-hint');

    // Undo twice: Opponent's latest move, followed by player's latest move
    undo();
    window.setTimeout(function () {
      undo();
      window.setTimeout(function () {
        showHint();
      }, 250);
    }, 250);
  } else {
    alert('Nothing to undo.');
  }
});

function redo() {
  game.move(undo_stack.pop());
  board.position(game.fen());
}



function removeGreySquares() {
  $('#myBoard .square-55d63').css('background', '');
}

function greySquare(square) {
  var $square = $('#myBoard .square-' + square);

  var background = whiteSquareGrey;
  if ($square.hasClass('black-3c85d')) {
    background = blackSquareGrey;
  }

  $square.css('background', background);
}

function onDragStart(source, piece) {
  // do not pick up pieces if the game is over
  if (game.game_over()) return false;

  // or if it's not that side's turn
  if (
    (game.turn() === 'w' && piece.search(/^b/) !== -1) ||
    (game.turn() === 'b' && piece.search(/^w/) !== -1)
  ) {
    return false;
  }
}

function updateAdvantage(score) {
  if (score > 0) {
    $('#advantageColor').text('Black');
    $('#advantageNumber').text(score);
  } else if (score < 0) {
    $('#advantageColor').text('White');
    $('#advantageNumber').text(-score);
  } else {
    $('#advantageColor').text('Neither side');
    $('#advantageNumber').text(score);
  }
  $('#advantageBar').attr({
    'aria-valuenow': `${-score}`,
    style: `width: ${((-score + 2000) / 4000) * 100}%`,
  });
}

function ajaxMove(move) {
  const body = {
    data: move,
  };

  $.ajax({
    headers: {
      'Content-Type': 'application/json',
      'Data-Type': 'json',
    },
    type: 'POST',
    url: '/api/move',
    data: JSON.stringify(body),
    success: function (data) {
      if (data.error) {
        ajaxStop();
      } else {
        const move = data.data.move;
        const score = data.data.score;
        console.log('SUCCESSSSS');
        console.log(data.data);
        updateAdvantage(score);
        game.move(move);
        checkStatus('white')
        board.position(game.fen());
      }
    },
    error: function (data) {
      console.log('ERRORRRRRRRR');
      console.log(data);
    }
  });
}

function onDrop(source, target) {
  checkStatus('black')
  undo_stack = [];
  removeGreySquares();
  var move = game.move({
    from: source,
    to: target,
    promotion: 'q', // NOTE: always promote to a queen for example simplicity
  });


  // Illegal move
  if (move === null) return 'snapback';

  // Send the move to the server
  ajaxMove(move);
}

function onMouseoverSquare(square, piece) {
  // get list of possible moves for this square
  var moves = game.moves({
    square: square,
    verbose: true,
  });

  // exit if there are no moves available for this square
  if (moves.length === 0) return;

  // highlight the square they moused over
  greySquare(square);

  // highlight the possible squares for this piece
  for (var i = 0; i < moves.length; i++) {
    greySquare(moves[i].to);
  }
}

function onMouseoutSquare(square, piece) {
  removeGreySquares();
}

function onSnapEnd() {
  board.position(game.fen());
}

