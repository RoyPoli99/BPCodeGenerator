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