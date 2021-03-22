// Assertions

function addAssertions(f, p) {

    bp.registerBThread("AssertWin(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">," + "<" + f[p[2]].x + "," + f[p[2]].y + ">)", function() {
        while (true) {
            let ev1 = bp.sync({ waitFor:[ O(f[p[0]].x, f[p[0]].y), X(f[p[2]].x, f[p[2]].y) ] });
            if (ev1.name.startsWith("X(")){
                break;
            }
            let ev2 = bp.sync({ waitFor:[ O(f[p[1]].x, f[p[1]].y), X(f[p[2]].x, f[p[2]].y) ] });
            if (ev2.name.startsWith("X(")){
                break;
            }
            let ev = bp.sync({ waitFor:[Omove, X(f[p[2]].x, f[p[2]].y)]});
            bp.ASSERT(ev.name.startsWith("X(") || ev.name.startsWith("O(" + f[p[2]].x + "," + f[p[2]].y + ")"), "WIN_VIOLATION");
        }
    });

    bp.registerBThread("AssertBlock(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">," + "<" + f[p[2]].x + "," + f[p[2]].y + ">)", function() {
        while (true) {

            let ev1 = bp.sync({ waitFor:[ X(f[p[0]].x, f[p[0]].y), O(f[p[2]].x, f[p[2]].y) ] });
            if (ev1.name.startsWith("O("))
                break;

            let ev2 = bp.sync({ waitFor:[ X(f[p[1]].x, f[p[1]].y), O(f[p[2]].x, f[p[2]].y) ] });
            if (ev2.name.startsWith("O("))
                break;

            let ev = bp.sync({ waitFor:[Omove]});
            let evNext = bp.sync({ waitFor:[Xmove, OWin]})
            bp.ASSERT(!evNext.name.startsWith("X(") || ev.name.startsWith("O(" + f[p[2]].x + "," + f[p[2]].y + ")"), "BLOCK_VIOLATION");
            //ask special event
            //sync({block: bp.all}) ??
        }
    });
}

lines.forEach(function(l) {
	perms.forEach(function(p) {
		addAssertions(l, p);
	});
});


bp.registerBThread("AddThirdO(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">," + "<" + f[p[2]].x + "," + f[p[2]].y + ">)", function () {
    while (true) {
        bp.sync({waitFor: [X(f[p[2]].x, f[p[2]].y)]});
        bp.sync({waitFor: [X(f[p[1]].x, f[p[1]].y)]});
        bp.sync({request: [O(f[p[0]].x, f[p[0]].y), O(f[p[1]].x, f[p[1]].y), O(f[p[0]].x, f[p[0]].y)]}, 10);
    }
});
bp.registerBThread("PreventThirdX(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">," + "<" + f[p[2]].x + "," + f[p[2]].y + ">)", function () {
    while (true) {
        bp.sync({waitFor: [O(f[p[2]].x, f[p[2]].y)]});
        bp.sync({waitFor: [O(f[p[1]].x, f[p[1]].y)]});
        bp.sync({request: [O(f[p[0]].x, f[p[0]].y), O(f[p[1]].x, f[p[1]].y)]}, 11);
    }
});
bp.registerBThread("PreventFork22X(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">)", function () {
    while (true) {
        bp.sync({waitFor: [X(f[p[1]].x, f[p[1]].y)]});
        bp.sync({waitFor: [X(f[p[1]].x, f[p[1]].y)]});
        bp.sync({request: [O(0, 0), O(2, 2)]}, 4);
    }
});
bp.registerBThread("PreventFork02X(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">)", function () {
    while (true) {
        bp.sync({request: [O(2, 2), O(0, 1), O(0, 2), O(0, 1)]}, 1);
    }
});
bp.registerBThread("PreventFork20X(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">)", function () {
    while (true) {
        bp.sync({request: [O(2, 2), O(0, 1), O(0, 2), O(2, 0)]}, 1);
    }
});
bp.registerBThread("PreventFork00X(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">)", function () {
    while (true) {
        bp.sync({waitFor: [X(f[p[1]].x, f[p[1]].y)]});
        bp.sync({request: [O(0, 2)]}, 1);
    }
});
bp.registerBThread("PreventForkdiagX(<" + f[p[0]].x + "," + f[p[0]].y + ">," + "<" + f[p[1]].x + "," + f[p[1]].y + ">)", function () {
    while (true) {
        bp.sync({request: [O(2, 2), O(0, 1), O(0, 2), O(2, 0)]}, 1);
    }
});
bp.registerBThread("Center", function () {
    while (true) {
        bp.sync({request: [O(1, 1), O(1, 0), O(0, 1)]}, 5);
    }
});
bp.registerBThread("Corners", function () {
    while (true) {
        bp.sync({request: [O(1, 1), O(2, 2), O(0, 2)]}, 9);
    }
});
bp.registerBThread("Sides", function () {
    while (true) {
        bp.sync({request: [O(1, 1), O(2, 2), O(0, 2)]}, 9);
    }
});

