package evoBP;

import il.ac.bgu.cs.bp.bpjs.execution.listeners.InMemoryEventLoggingListener;
import il.ac.bgu.cs.bp.bpjs.model.BEvent;
import il.ac.bgu.cs.bp.bpjs.execution.BProgramRunner;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;
import java.util.stream.DoubleStream;
import java.util.stream.IntStream;

public class RunnerEvaluatorOrg extends Evaluator {
    private static ExecutorService es = Executors.newCachedThreadPool();

    public RunnerEvaluatorOrg(String code, int gen, int id) {
        super(code, gen, id, gen > 500 ? "opt" : "rand");
    }

    @Override
    protected Bp.EvaluationResponse evaluate() {
        double[][][][] res = run_games();
        Bp.EvaluationResponse.Builder builder = Bp.EvaluationResponse.newBuilder()
                .setWins(res[0][0][0][0])
                .setLosses(res[0][0][0][1])
                .setDraws(res[0][0][0][2])
                .setBlocksViolations(res[0][0][0][3])
                .setMisses(res[0][0][0][4])
                .setBlocks(res[0][0][0][5])
                .setDeadlocks(res[0][0][0][6])
                .setForks(res[0][0][0][7])
                .setForksViolations(res[0][0][0][8]);
        builder.addAllWinO(CreateNestedList(res, 1));
        builder.addAllWinV(CreateNestedList(res, 2));
        builder.addAllBlockO(CreateNestedList(res, 3));
        builder.addAllBlockV(CreateNestedList(res, 4));
        builder.addAllForkO(CreateNestedList(res, 5));
        builder.addAllForkV(CreateNestedList(res, 6));
        builder.addAllRequests(CreateNestedList(res, 7));
        return builder.build();
    }

    private List<Bp.innerinnerType> CreateNestedList(double[][][][] res, int type){
        List<Bp.innerinnerType> innerinnerBuilders = new LinkedList<>();
        for(int s=0; s<10; s++){
            List<Bp.innerType> innerBuilders = new LinkedList<>();
            for(int t=0; t<5; t++){
                Bp.innerType.Builder innerBuilder = Bp.innerType.newBuilder();
                innerBuilder.addAllFoo(DoubleStream.of(res[type][s][t]).boxed().collect(Collectors.toList()));
                innerBuilders.add(innerBuilder.build());
            }
            Bp.innerinnerType.Builder innerInnerBuilder = Bp.innerinnerType.newBuilder();
            innerInnerBuilder.addAllFoo(innerBuilders);
            innerinnerBuilders.add(innerInnerBuilder.build());
        }
        return innerinnerBuilders;
    }

    private double[][][][] run_games() {
        AtomicInteger wins = new AtomicInteger();
        AtomicInteger losses = new AtomicInteger();
        AtomicInteger draws = new AtomicInteger();
        AtomicInteger blocks_violations = new AtomicInteger();
        AtomicInteger misses = new AtomicInteger();
        AtomicInteger blocks = new AtomicInteger();
        AtomicInteger forks = new AtomicInteger();
        AtomicInteger forks_violations = new AtomicInteger();
        LinkedList<Integer> sets = new LinkedList();
        LinkedList<Integer> threads = new LinkedList();
        LinkedList<Integer> inputs = new LinkedList();
        // 3D array structures is set-thread-input
        double[][][] block_violations_list = new double[10][5][9];
        double[][][] win_violations_list = new double[10][5][9];
        double[][][] fork_violations_list = new double[10][5][9];
        double[][][] blocks_observances = new double[10][5][9];
        double[][][] wins_observances = new double[10][5][9];
        double[][][] forks_block_observances = new double[10][5][9];
        double[][][] requests = new double[10][5][9];
        for (int i = 0; i < 100; i++) {
            InMemoryEventLoggingListener logger = new InMemoryEventLoggingListener();
            String player_type;
            if(i < 10)
                player_type = "opt_x";
            else
                if(i < 20)
                    player_type = "opt_o";
                else
                    if(i < 60)
                        player_type = "rand_x";
                    else
                        player_type = "rand_o";
            BProgramRunner brunner = new BProgramRunner(BProgramFactory(player_type));
            brunner.addListener(logger);
            brunner.run();
            List<BEvent> events = logger.getEvents();
            String line = "Generation" + gen + "_Game" + i + ": ";
            String extra = "";
            for (BEvent ev : events) {
                switch (ev.name) {
                    case "OWin":
                        wins.getAndIncrement();
                        for(int j= 0; j < sets.size(); j++){
                            wins_observances[sets.get(j)][threads.get(j)][inputs.get(j)]++;
                        }
                        break;
                    case "XWin":
                        losses.getAndIncrement();
                        break;
                    case "Draw":
                        draws.getAndIncrement();
                        break;
                    case "BLOCK_VIOLATION":
                        blocks_violations.getAndIncrement();
                        for(int j= 0; j < sets.size(); j++){
                            block_violations_list[sets.get(j)][threads.get(j)][inputs.get(j)]++;
                        }
                        break;
                    case "WIN_VIOLATION":
                        misses.getAndIncrement();
                        for(int j= 0; j < sets.size(); j++){
                            win_violations_list[sets.get(j)][threads.get(j)][inputs.get(j)]++;
                        }
                        break;
                    case "FORK_VIOLATION":
                        forks_violations.getAndIncrement();
                        for(int j= 0; j < sets.size(); j++){
                            fork_violations_list[sets.get(j)][threads.get(j)][inputs.get(j)]++;
                        }
                        break;
                    case "FORK":
                        forks.getAndIncrement();
                        for(int j= 0; j < sets.size(); j++){
                            forks_block_observances[sets.get(j)][threads.get(j)][inputs.get(j)]++;
                        }
                        break;
                    case "BLOCK":
                        blocks.getAndIncrement();
                        for(int j= 0; j < sets.size(); j++){
                            blocks_observances[sets.get(j)][threads.get(j)][inputs.get(j)]++;
                        }
                        break;
                    case "X":
                        if(id == 1) {
                            Map<String, Number> data = (Map<String, Number>) ev.maybeData;
                            extra = "(" + data.get("row").intValue() + "," + data.get("col").intValue() + ")";
                        }
                        break;
                    case "O":
                        sets.clear();
                        threads.clear();
                        inputs.clear();
                        if(id == 1) {
                            Map<String, Number> data2 = (Map<String, Number>) ev.maybeData;
                            extra = "(" + data2.get("row").intValue() + "," + data2.get("col").intValue() + ")";
                        }
                        break;
                    default:
                        int set_index = Character.getNumericValue(ev.name.charAt(4));
                        int thread_index = Character.getNumericValue(ev.name.charAt(13));
                        int input_index = Character.getNumericValue(ev.name.charAt(21));
                        sets.add(set_index);
                        threads.add(thread_index);
                        inputs.add(input_index);
                        requests[set_index][thread_index][input_index]++;
                        break;
                }
                if(id == 1) {
                    line += ev.name + extra + ", ";
                    extra = "";
                }
            }
            if(id == 1) {
                System.out.println(line);
            }
        }
        //});
        double deadlocks = 100 - wins.get() - losses.get() - draws.get();
        double[][][] results = new double[][][]{{{wins.get(), losses.get(), draws.get(), blocks_violations.get(), misses.get(), blocks.get(), deadlocks, forks.get(), forks_violations.get() }}};
        return new double[][][][]{results, wins_observances, win_violations_list, blocks_observances, block_violations_list, forks_block_observances, fork_violations_list, requests};

    }
}
