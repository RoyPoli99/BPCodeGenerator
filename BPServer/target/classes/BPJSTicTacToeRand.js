function Move(row, col, type){
	return bp.Event(type + "(" + row + "," + col + ")", {row:row, col:col});
}
function X(row, col) {
	return Move(row, col, "X");
}
function O(row, col) {
	return Move(row, col, "O");
}
var XWin = bp.Event("XWin");
var OWin = bp.Event("OWin");
var draw = bp.Event("Draw");
var gameOver = bp.Event("GameOver");
// GameRules:
function addSquareBThreads(row, col) {
	bp.registerBThread("RandomXPlayer(" + row + "," + col + ")", function () {
		bp.sync({request:[X(row, col)]});
	});
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
bp.registerBThread("EnforceTurns", function() {
	while (true) {
		bp.sync({ waitFor:[ X(0, 0), X(0, 1), X(0, 2),
				X(1, 0), X(1, 1), X(1, 2),
				X(2, 0), X(2, 1), X(2, 2) ],
			block:[ O(0, 0), O(0, 1), O(0, 2),
				O(1, 0), O(1, 1), O(1, 2),
				O(2, 0), O(2, 1), O(2, 2) ] });

		bp.sync({ waitFor:[ O(0, 0), O(0, 1), O(0, 2), O(1, 0), O(1, 1), O(1, 2), O(2, 0), O(2, 1), O(2, 2) ],
			block:[ X(0, 0), X(0, 1), X(0, 2), X(1, 0), X(1, 1), X(1, 2), X(2, 0), X(2, 1), X(2, 2) ] });
	}
});

// Represents when the game ends
bp.registerBThread("EndOfGame", function() {
	bp.sync({ waitFor:[ OWin, XWin, draw ] });

	bp.sync({ block:[ X(0, 0), X(0, 1), X(0, 2),
			X(1, 0), X(1, 1), X(1, 2),
			X(2, 0), X(2, 1), X(2, 2),
			O(0, 0), O(0, 1), O(0, 2),
			O(1, 0), O(1, 1), O(1, 2),
			O(2, 0), O(2, 1), O(2, 2),
			OWin, XWin, draw] });
});

var move = bp.EventSet("Move events", function(e) {
	//return e instanceof Move;
	return e.name.startsWith("X(") || e.name.startsWith("O(");
});

// Represents when it is a draw
bp.registerBThread("DetectDraw", function() {
	// For debug
	bp.sync({ waitFor:[ move ] });
	bp.sync({ waitFor:[ move ] });
	bp.sync({ waitFor:[ move ] });

	bp.sync({ waitFor:[ move ] });
	bp.sync({ waitFor:[ move ] });
	bp.sync({ waitFor:[ move ] });

	bp.sync({ waitFor:[ move ] });
	bp.sync({ waitFor:[ move ] });
	bp.sync({ waitFor:[ move ] });
	/*
	 * for (var i=0; i< 9; i++) { bp.sync({ waitFor:[ move ] }); }
	 */

	bp.sync({ request:[ draw ] }, 90);
});

function addLinePermutationBthreads(f, p) {

	// Represents when X wins
	bp.registerBThread("DetectXWin(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">," + "<" + f[p[2]].x + "," + f[p[2]].y + ">)", function() {
		while (true) {
			bp.sync({ waitFor:[ X(f[p[0]].x, f[p[0]].y) ] });

			bp.sync({ waitFor:[ X(f[p[1]].x, f[p[1]].y) ] });

			bp.sync({ waitFor:[ X(f[p[2]].x, f[p[2]].y) ] });

			bp.sync({ request:[ XWin ] }, 100);

		}
	});

	// Represents when O wins
	bp.registerBThread("DetectOWin(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">," + "<" + f[p[2]].x + "," + f[p[2]].y + ">)", function() {
		while (true) {
			bp.sync({ waitFor:[ O(f[p[0]].x, f[p[0]].y) ] });

			bp.sync({ waitFor:[ O(f[p[1]].x, f[p[1]].y) ] });

			bp.sync({ waitFor:[ O(f[p[2]].x, f[p[2]].y) ] });

			bp.sync({ request:[ OWin ] }, 100);

		}
	});

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
	// Player O strategy to prevent the Fork22 of player X
	bThread2
}

function addFork02PermutationBthreads(f, p) {
	// Player O strategy to prevent the Fork02 of player X
	bThread3
}

function addFork20PermutationBthreads(f, p) {
	// Player O strategy to prevent the Fork20 of player X
	bThread4
}

function addFork00PermutationBthreads(f, p) {
	// Player O strategy to prevent the Fork00 of player X
	bThread5
}

function addForkdiagPermutationBthreads(f, p) {
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

// Preference to put O on the center
bThread7

// Preference to put O on the corners
bThread8

// Preference to put O on the sides
bThread9
