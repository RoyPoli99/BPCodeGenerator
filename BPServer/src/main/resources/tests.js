function behaviorSet1(input) {
    bp.registerBThread("O_Player_Thread_1_1", function(){
        bp.sync({request:[O(input[0].x, input[0].y)]},5);
    });

    bp.registerBThread("O_Player_Thread_1_2", function(){
        bp.sync({waitFor:[O(input[0].x, input[0].y), X(input[2].x, input[2].y)]});
        bp.sync({waitFor:[X(input[0].x, input[0].y), X(input[1].x, input[1].y)]});
        bp.sync({request:[O(input[2].x, input[2].y), O(input[2].x, input[2].y)]},9);
    });

    bp.registerBThread("O_Player_Thread_1_3", function(){
        bp.sync({waitFor:[O(input[2].x, input[2].y), X(input[1].x, input[1].y), X(input[1].x, input[1].y), X(input[1].x, input[1].y)]});
        bp.sync({waitFor:[X(input[0].x, input[0].y)]});
        bp.sync({request:[O(input[1].x, input[1].y), O(input[1].x, input[1].y), O(input[3].x, input[3].y), O(input[2].x, input[2].y)]},8);
    });

}
var inputs_1 = [[{x: 0, y: 0}, {x: 0, y: 2}, {x: 2, y: 0}, {x: 1, y: 1}],
    [{x: 1, y: 2}, {x: 1, y: 0}, {x: 2, y: 1}, {x: 1, y: 0}],
    [{x: 2, y: 1}, {x: 2, y: 1}, {x: 0, y: 0}, {x: 1, y: 0}],
    [{x: 0, y: 1}, {x: 0, y: 1}, {x: 1, y: 0}, {x: 0, y: 0}],
    [{x: 1, y: 0}, {x: 1, y: 2}, {x: 1, y: 1}, {x: 2, y: 0}],
    [{x: 0, y: 2}, {x: 0, y: 0}, {x: 1, y: 0}, {x: 2, y: 2}],
    [{x: 1, y: 0}, {x: 2, y: 0}, {x: 0, y: 1}, {x: 0, y: 2}],
    [{x: 0, y: 0}, {x: 0, y: 0}, {x: 2, y: 1}, {x: 1, y: 2}]]
inputs_1.forEach(function (input) {
    behaviorSet1(input);
});

function behaviorSet2(input) {
    bp.registerBThread("O_Player_Thread_2_1", function(){
        bp.sync({waitFor:[X(input[1].x, input[1].y), X(input[1].x, input[1].y), X(input[2].x, input[2].y)]});
        bp.sync({waitFor:[O(input[0].x, input[0].y)]});
        bp.sync({request:[O(input[2].x, input[2].y), O(input[4].x, input[4].y)]},5);
    });

    bp.registerBThread("O_Player_Thread_2_2", function(){
        bp.sync({waitFor:[O(input[1].x, input[1].y), X(input[0].x, input[0].y)]});
        bp.sync({request:[O(input[3].x, input[3].y), O(input[0].x, input[0].y)]},1);
    });

    bp.registerBThread("O_Player_Thread_2_3", function(){
        bp.sync({request:[O(input[4].x, input[4].y), O(input[4].x, input[4].y), O(input[2].x, input[2].y), O(input[0].x, input[0].y)]},5);
    });

}
var inputs_2 = [[{x: 2, y: 2}, {x: 0, y: 1}, {x: 2, y: 2}, {x: 2, y: 2}, {x: 2, y: 1}, {x: 0, y: 0}],
    [{x: 1, y: 2}, {x: 1, y: 0}, {x: 1, y: 0}, {x: 1, y: 1}, {x: 2, y: 1}, {x: 0, y: 2}],
    [{x: 2, y: 0}, {x: 1, y: 2}, {x: 1, y: 2}, {x: 2, y: 1}, {x: 0, y: 2}, {x: 0, y: 2}]]
inputs_2.forEach(function (input) {
    behaviorSet2(input);
});

function behaviorSet3(input) {
    bp.registerBThread("O_Player_Thread_3_1", function(){
        bp.sync({waitFor:[X(input[2].x, input[2].y), X(input[3].x, input[3].y)]});
        bp.sync({waitFor:[X(input[0].x, input[0].y)]});
        bp.sync({request:[O(input[1].x, input[1].y)]},4);
    });

}
var inputs_3 = [[{x: 1, y: 2}, {x: 1, y: 0}, {x: 2, y: 1}, {x: 0, y: 1}, {x: 0, y: 2}],
    [{x: 0, y: 0}, {x: 1, y: 2}, {x: 0, y: 1}, {x: 1, y: 2}, {x: 2, y: 0}],
    [{x: 0, y: 1}, {x: 0, y: 2}, {x: 2, y: 0}, {x: 1, y: 2}, {x: 1, y: 0}]]
inputs_3.forEach(function (input) {
    behaviorSet3(input);
});

function behaviorSet4(input) {
    bp.registerBThread("O_Player_Thread_4_1", function(){
        bp.sync({request:[O(input[1].x, input[1].y)]},11);
    });

}
var inputs_4 = [[{x: 2, y: 0}, {x: 0, y: 0}, {x: 2, y: 1}, {x: 0, y: 1}, {x: 2, y: 0}],
    [{x: 0, y: 0}, {x: 0, y: 1}, {x: 1, y: 2}, {x: 2, y: 2}, {x: 2, y: 2}],
    [{x: 1, y: 0}, {x: 0, y: 2}, {x: 2, y: 0}, {x: 1, y: 1}, {x: 2, y: 2}]]
inputs_4.forEach(function (input) {
    behaviorSet4(input);
});

function behaviorSet5(input) {
    bp.registerBThread("O_Player_Thread_5_1", function(){
        bp.sync({waitFor:[O(input[1].x, input[1].y), O(input[1].x, input[1].y), O(input[1].x, input[1].y)]});
        bp.sync({waitFor:[O(input[6].x, input[6].y), O(input[3].x, input[3].y), O(input[5].x, input[5].y), O(input[1].x, input[1].y)]});
        bp.sync({request:[O(input[6].x, input[6].y)]},9);
    });

    bp.registerBThread("O_Player_Thread_5_2", function(){
        bp.sync({waitFor:[O(input[2].x, input[2].y), X(input[2].x, input[2].y), O(input[1].x, input[1].y), O(input[7].x, input[7].y)]});
        bp.sync({request:[O(input[5].x, input[5].y), O(input[3].x, input[3].y), O(input[0].x, input[0].y), O(input[8].x, input[8].y)]},5);
    });

    bp.registerBThread("O_Player_Thread_5_3", function(){
        bp.sync({waitFor:[O(input[1].x, input[1].y), O(input[1].x, input[1].y), O(input[1].x, input[1].y)]});
        bp.sync({waitFor:[O(input[6].x, input[6].y), O(input[3].x, input[3].y), O(input[5].x, input[5].y), O(input[1].x, input[1].y)]});
        bp.sync({request:[O(input[5].x, input[5].y), O(input[3].x, input[3].y), O(input[0].x, input[0].y), O(input[8].x, input[8].y)]},8);
    });

}
var inputs_5 = [[{x: 2, y: 0}, {x: 0, y: 1}, {x: 0, y: 1}, {x: 2, y: 2}, {x: 0, y: 1}, {x: 1, y: 2}, {x: 2, y: 2}, {x: 2, y: 1}, {x: 2, y: 1}]]
inputs_5.forEach(function (input) {
    behaviorSet5(input);
});

function behaviorSet6(input) {
    bp.registerBThread("O_Player_Thread_6_1", function(){
        bp.sync({waitFor:[X(input[1].x, input[1].y), X(input[1].x, input[1].y), X(input[0].x, input[0].y)]});
        bp.sync({request:[O(input[1].x, input[1].y), O(input[1].x, input[1].y), O(input[0].x, input[0].y), O(input[0].x, input[0].y)]},9);
    });

    bp.registerBThread("O_Player_Thread_6_2", function(){
        bp.sync({waitFor:[X(input[1].x, input[1].y)]});
        bp.sync({waitFor:[X(input[1].x, input[1].y)]});
        bp.sync({request:[O(input[0].x, input[0].y)]},7);
    });

}
var inputs_6 = [[{x: 2, y: 2}, {x: 2, y: 0}],
    [{x: 1, y: 0}, {x: 1, y: 1}],
    [{x: 1, y: 1}, {x: 2, y: 0}],
    [{x: 2, y: 1}, {x: 2, y: 1}],
    [{x: 2, y: 1}, {x: 2, y: 0}],
    [{x: 1, y: 0}, {x: 0, y: 1}]]
inputs_6.forEach(function (input) {
    behaviorSet6(input);
});

function behaviorSet7(input) {
    bp.registerBThread("O_Player_Thread_7_1", function(){
        bp.sync({waitFor:[O(input[0].x, input[0].y), X(input[1].x, input[1].y), O(input[2].x, input[2].y)]});
        bp.sync({request:[O(input[3].x, input[3].y)]},5);
    });

}
var inputs_7 = [[{x: 0, y: 0}, {x: 0, y: 2}, {x: 1, y: 0}, {x: 1, y: 2}],
    [{x: 1, y: 1}, {x: 1, y: 0}, {x: 0, y: 0}, {x: 1, y: 0}],
    [{x: 1, y: 2}, {x: 0, y: 0}, {x: 2, y: 1}, {x: 2, y: 2}],
    [{x: 0, y: 0}, {x: 0, y: 2}, {x: 2, y: 0}, {x: 1, y: 1}],
    [{x: 0, y: 1}, {x: 2, y: 0}, {x: 2, y: 1}, {x: 2, y: 1}],
    [{x: 0, y: 2}, {x: 0, y: 2}, {x: 0, y: 0}, {x: 2, y: 1}],
    [{x: 1, y: 0}, {x: 0, y: 1}, {x: 2, y: 1}, {x: 0, y: 2}],
    [{x: 2, y: 2}, {x: 0, y: 0}, {x: 0, y: 2}, {x: 2, y: 0}]]
inputs_7.forEach(function (input) {
    behaviorSet7(input);
});


