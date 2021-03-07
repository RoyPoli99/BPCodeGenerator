function Move(row, col, type) {
	return bp.Event(type, {row: row, col: col});
}

function X(row, col) {
	return Move(row, col, "X");
}

function O(row, col) {
	return Move(row, col, "O");
}

var move = bp.EventSet("Move events", function (e) {
	//return e instanceof Move;
	return e.name == 'X' || e.name == "O";
});

var Xmove = bp.EventSet("X events", function (e) {
	//return e instanceof Move;
	return e.name == "X"
});

var Omove = bp.EventSet("O events", function (e) {
	//return e instanceof Move;
	return e.name == "O"
});

var XWin = bp.Event("XWin");
var OWin = bp.Event("OWin");
var draw = bp.Event("Draw");
var gameOver = bp.EventSet("GameOver", function (e) {
	return e.equals(XWin) || e.equals(OWin) || e.equals(draw);
});

// GameRules:

// This BThreads are on each square of the grid
function addSquareBThreads(row, col) {
	// Blocks further marking of a square already marked by X or O.
	bp.registerBThread("SquareTaken(" + row + "," + col + ")", function() {
		while (true) {
			bp.sync({ waitFor:[ X(row, col), O(row, col) ] });
			bp.sync({ block:[ X(row, col), O(row, col) ] });
		}
	});
}

for (var r = 0; r < 3; r++) {
	for (var c = 0; c < 3; c++) {
		addSquareBThreads(r, c);
	}
}

// Represents Enforce Turns
bp.registerBThread("EnforceTurns", function () {
	while (true) {
		bp.sync({waitFor: Xmove, block: Omove});
		bp.sync({waitFor: Omove, block: Xmove});
	}
});

// Represents when the game ends
bp.registerBThread("EndOfGame", function () {
	bp.sync({waitFor: gameOver})
	bp.sync({block: bp.all})
});

// Represents when it is a draw
bp.registerBThread("DetectDraw", function () {
	for (var i = 0; i < 9; i++) {
		bp.sync({waitFor: move})
	}
	bp.sync({request: draw}, 90);
});

function addLinePermutationBthreads(f, p) {

	// Represents when X wins
	bp.registerBThread("DetectXWin(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">," + "<" + f[p[2]].x + "," + f[p[2]].y + ">)", function() {
		while (true) {
			bp.sync({ waitFor:[ X(f[p[0]].x, f[p[0]].y) ] });

			bp.sync({ waitFor:[ X(f[p[1]].x, f[p[1]].y) ] });

			bp.sync({ waitFor:[ X(f[p[2]].x, f[p[2]].y) ] });

			bp.sync({ request: XWin }, 100);

		}
	});

	// Represents when O wins
	bp.registerBThread("DetectOWin(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">," + "<" + f[p[2]].x + "," + f[p[2]].y + ">)", function() {
		while (true) {
			bp.sync({ waitFor:[ O(f[p[0]].x, f[p[0]].y) ] });

			bp.sync({ waitFor:[ O(f[p[1]].x, f[p[1]].y) ] });

			bp.sync({ waitFor:[ O(f[p[2]].x, f[p[2]].y) ] });

			bp.sync({request: OWin}, 100);

		}
	});

	//Player X is now playing at optimal strategy: *******************************************************
	// Player X strategy to add a the third X to win
	bp.registerBThread("AddThirdX(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">," + "<" + f[p[2]].x + "," + f[p[2]].y + ">)", function() {
		while (true) {
			bp.sync({ waitFor:[ X(f[p[0]].x, f[p[0]].y) ] });

			bp.sync({ waitFor:[ X(f[p[1]].x, f[p[1]].y) ] });

			bp.sync({ request:[ X(f[p[2]].x, f[p[2]].y) ] }, 50);
		}
	});

	// Player X strategy to prevent the third O of player O
	bp.registerBThread("PreventThirdO(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">," + "<" + f[p[2]].x + "," + f[p[2]].y + ">)", function() {
		while (true) {
			bp.sync({ waitFor:[ O(f[p[0]].x, f[p[0]].y) ] });

			bp.sync({ waitFor:[ O(f[p[1]].x, f[p[1]].y) ] });

			bp.sync({ request:[ X(f[p[2]].x, f[p[2]].y) ] }, 40);
		}
	});
	//Player X is now playing at optimal strategy done adding *******************************************************

	// Player O strategy to add a the third O to win
	bThread0

	// Player O strategy to prevent the third X of player X
	bThread1
}

// Player O strategy:

var lines = [ [ { x:0, y:0 }, { x:0, y:1 }, { x:0, y:2 } ],
	[ { x:1, y:0 }, { x:1, y:1 }, { x:1, y:2 } ],
	[ { x:2, y:0 }, { x:2, y:1 }, { x:2, y:2 } ],
	[ { x:0, y:0 }, { x:1, y:0 }, { x:2, y:0 } ],
	[ { x:0, y:1 }, { x:1, y:1 }, { x:2, y:1 } ],
	[ { x:0, y:2 }, { x:1, y:2 }, { x:2, y:2 } ],
	[ { x:0, y:0 }, { x:1, y:1 }, { x:2, y:2 } ],
	[ { x:0, y:2 }, { x:1, y:1 }, { x:2, y:0 } ] ];
var perms = [ [ 0, 1, 2 ], [ 0, 2, 1 ], [ 1, 0, 2 ],
	[ 1, 2, 0 ], [ 2, 0, 1 ], [ 2, 1, 0 ] ];

lines.forEach(function(l) {
	perms.forEach(function(p) {
		addLinePermutationBthreads(l, p);
	});
});

function addFork22PermutationBthreads(f, p) {

	// Player X strategy to prevent the Fork22 of player O
	bp.registerBThread("PreventFork22O(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">)", function() {
		while (true) {
			bp.sync({ waitFor:[ O(f[p[0]].x, f[p[0]].y) ] });

			bp.sync({ waitFor:[ O(f[p[1]].x, f[p[1]].y) ] });

			bp.sync({ request:[ X(2, 2), X(0,2), X(2,0) ] }, 30);
		}
	});

	// Player O strategy to prevent the Fork22 of player X
	bThread2
}

function addFork02PermutationBthreads(f, p) {
	// Player X strategy to prevent the Fork02 of player O
	bp.registerBThread("PreventFork02O(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">)", function() {
		while (true) {
			bp.sync({ waitFor:[ O(f[p[0]].x, f[p[0]].y) ] });

			bp.sync({ waitFor:[ O(f[p[1]].x, f[p[1]].y) ] });

			bp.sync({ request:[ X(0, 2), X(0,0), X(2,2) ] }, 30);
		}
	});

	// Player O strategy to prevent the Fork02 of player X
	bThread3
}

function addFork20PermutationBthreads(f, p) {
	// Player X strategy to prevent the Fork20 of player O
	bp.registerBThread("PreventFork20O(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">)", function() {
		while (true) {
			bp.sync({ waitFor:[ O(f[p[0]].x, f[p[0]].y) ] });

			bp.sync({ waitFor:[ O(f[p[1]].x, f[p[1]].y) ] });

			bp.sync({ request:[ X(2, 0), X(0,0), X(2,2) ] }, 30);
		}
	});


	// Player O strategy to prevent the Fork20 of player X
	bThread4
}

function addFork00PermutationBthreads(f, p) {
	// Player X strategy to prevent the Fork00 of player O
	bp.registerBThread("PreventFork00O(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">)", function() {
		while (true) {
			bp.sync({ waitFor:[ O(f[p[0]].x, f[p[0]].y) ] });

			bp.sync({ waitFor:[ O(f[p[1]].x, f[p[1]].y) ] });

			bp.sync({ request:[ X(0, 0), X(0,2), X(2,0) ] }, 30);
		}
	});


	// Player O strategy to prevent the Fork00 of player X
	bThread5
}

function addForkdiagPermutationBthreads(f, p) {
	// Player X strategy to prevent the Forkdiagonal of player O
	bp.registerBThread("PreventForkdiagO(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">)", function() {
		while (true) {
			bp.sync({ waitFor:[ O(f[p[0]].x, f[p[0]].y) ] });

			bp.sync({ waitFor:[ O(f[p[1]].x, f[p[1]].y) ] });

			bp.sync({ request:[ X(0, 1), X(1, 0), X(1, 2), X(2, 1) ] }, 30);
		}
	});


	// Player O strategy to prevent the Forkdiagonal of player X
	bThread6
}

var forks22 = [ [ { x:1, y:2 }, { x:2, y:0 } ], [ { x:2, y:1 }, { x:0, y:2 } ], [ { x:1, y:2 }, { x:2, y:1 } ] ];
var forks02 = [ [ { x:1, y:2 }, { x:0, y:0 } ], [ { x:0, y:1 }, { x:2, y:2 } ], [ { x:1, y:2 }, { x:0, y:1 } ] ];
var forks20 = [ [ { x:1, y:0 }, { x:2, y:2 } ], [ { x:2, y:1 }, { x:0, y:0 } ], [ { x:2, y:1 }, { x:1, y:0 } ] ];
var forks00 = [ [ { x:0, y:1 }, { x:2, y:0 } ], [ { x:1, y:0 }, { x:0, y:2 } ], [ { x:0, y:1 }, { x:1, y:0 } ] ];

var forksdiag = [ [ { x:0, y:2 }, { x:2, y:0 } ]
	//,[ { x:0, y:0 },{ x:2, y:2 }] // <--- Intentional BUG
];

var permsforks = [ [ 0, 1 ], [ 1, 0 ] ];

forks22.forEach(function(f) {
	permsforks.forEach(function(p) {
		addFork22PermutationBthreads(f, p);
	});
});

forks02.forEach(function(f) {
	permsforks.forEach(function(p) {
		addFork02PermutationBthreads(f, p);
	});
});

forks20.forEach(function(f) {
	permsforks.forEach(function(p) {
		addFork20PermutationBthreads(f, p);
	});
});

forks00.forEach(function(f) {
	permsforks.forEach(function(p) {
		addFork00PermutationBthreads(f, p);
	});
});

forksdiag.forEach(function(f) {
	permsforks.forEach(function(p) {
		addForkdiagPermutationBthreads(f, p);
	});
});

// Preference to put X on the center
bp.registerBThread("CenterX", function() {
	while (true) {
		bp.sync({ request:[ X(1, 1) ] }, 35);
	}
});

// Preference to put O on the center
bThread7

// Preference to put X on the corners
bp.registerBThread("CornersX", function() {
	while (true) {
		bp.sync({ request:[ X(0, 0), X(0, 2), X(2, 0), X(2, 2) ] }, 20);

	}
});

// Preference to put O on the corners
bThread8

// Preference to put X on the sides
bp.registerBThread("SidesX", function() {
	while (true) {
		bp.sync({ request:[ X(0, 1), X(1, 0), X(1, 2), X(2, 1) ] }, 10);
	}
});

// Preference to put O on the sides
bThread9


// Assertions
function addAssertions(f, p) {

	bp.registerBThread("AssertWin(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">," + "<" + f[p[2]].x + "," + f[p[2]].y + ">)", function () {

		//let ev1 = bp.sync({waitFor: [O(f[p[0]].x, f[p[0]].y), X(f[p[2]].x, f[p[2]].y)]})
		if(bp.sync({waitFor: [O(f[p[0]].x, f[p[0]].y), X(f[p[2]].x, f[p[2]].y)]}).name.equals('X')) {
			return;
		}
		//let ev2 = bp.sync({waitFor: [O(f[p[1]].x, f[p[1]].y), X(f[p[2]].x, f[p[2]].y)]});
		if(bp.sync({waitFor: [O(f[p[1]].x, f[p[1]].y), X(f[p[2]].x, f[p[2]].y)]}).name.equals('X')){
			return;
		}
		//if (ev2.name == 'X') {
		//  return;
		//}
		//let ev = bp.sync({waitFor: [Omove, X(f[p[2]].x, f[p[2]].y)]});
		while(true) {
			if (bp.sync({waitFor: [Omove, X(f[p[2]].x, f[p[2]].y)]}).name.equals('X')) {
				//x blocked the win - no violation
				return;
			} else {
				if (bp.sync({waitFor: [OWin, Xmove]}).name.equals('X')) {
					//x moved again, was not win
					bp.sync({request: bp.Event("WIN_VIOLATION")}, 110);
				} else {
					//was a win
					return;
				}
			}
		}
		//bp.ASSERT(ev.name.startsWith("X(") || ev.name.startsWith("O(" + f[p[2]].x + "," + f[p[2]].y + ")"), "WIN_VIOLATION");
		/*if(!(ev.name.startsWith("X(") || ev.name.startsWith("O(" + f[p[2]].x + "," + f[p[2]].y + ")"))){
          bp.sync({request: bp.Event("WIN_VIOLATION")}, 110);
        }*/
	});

	bp.registerBThread("AssertBlock(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">," + "<" + f[p[2]].x + "," + f[p[2]].y + ">)", function () {
		//let ev1 = bp.sync({waitFor: [X(f[p[0]].x, f[p[0]].y), O(f[p[2]].x, f[p[2]].y)]});
		if (bp.sync({waitFor: [X(f[p[0]].x, f[p[0]].y), O(f[p[2]].x, f[p[2]].y)]}).name.equals("O"))
			return;

		//let ev2 = bp.sync({waitFor: [X(f[p[1]].x, f[p[1]].y), O(f[p[2]].x, f[p[2]].y)]});
		if (bp.sync({waitFor: [X(f[p[1]].x, f[p[1]].y), O(f[p[2]].x, f[p[2]].y)]}).name.equals("O"))
			return;

		// let ev = bp.sync({waitFor: [Omove]});
		// let evNext = bp.sync({waitFor: [Xmove, OWin]})
		// //bp.ASSERT(!evNext.name.startsWith("X(") || ev.name.startsWith("O(" + f[p[2]].x + "," + f[p[2]].y + ")"), "BLOCK_VIOLATION");
		// if(!(!evNext.name.startsWith("X(") || ev.name.startsWith("O(" + f[p[2]].x + "," + f[p[2]].y + ")"))){
		//   bp.sync({request: bp.Event("BLOCK_VIOLATION")}, 110);
		// }


		while (true) {
			if (bp.sync({waitFor: [O(f[p[2]].x, f[p[2]].y), Xmove]}).name.equals('X')) {
				//O was not placed to block
				bp.sync({request: bp.Event("BLOCK_VIOLATION")}, 110);
			} else {
				//blocked win
				return;
			}
		}
	});
}

lines.forEach(function (l) {
	perms.forEach(function (p) {
		addAssertions(l, p);
	});
});
