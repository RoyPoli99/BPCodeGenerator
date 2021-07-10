package evoBP;

import il.ac.bgu.cs.bp.bpjs.execution.listeners.InMemoryEventLoggingListener;
import il.ac.bgu.cs.bp.bpjs.model.BEvent;
import il.ac.bgu.cs.bp.bpjs.execution.BProgramRunner;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

public class RunnerEvaluatorOrg extends Evaluator {
    private static ExecutorService es = Executors.newCachedThreadPool();

    public RunnerEvaluatorOrg(String code, int gen, int id, int threads) {
        super(code, gen, id, gen > 500 ? "opt" : "rand", threads);
    }

    @Override
    protected Bp.EvaluationResponse evaluate() {
        double[][] res = run_games();
        Bp.EvaluationResponse.Builder builder = Bp.EvaluationResponse.newBuilder()
                .setWins(res[0][0])
                .setLosses(res[0][1])
                .setDraws(res[0][2])
                .setBlocksViolations(res[0][3])
                .setMisses(res[0][4])
                .setBlocks(res[0][5])
                .setDeadlocks(res[0][6])
                .setForks(res[0][7]);
        for(int i=0; i<this.threads; i++){
            builder.addBlockV(res[1][i]);
            builder.addWinV(res[2][i]);
            builder.addForkV(res[3][i]);
            builder.addBlockG(res[4][i]);
            builder.addWinG(res[5][i]);
            builder.addForkG(res[6][i]);
            builder.addRequests(res[7][i]);
        }
        return builder.build();
    }

    private double[][] run_games() {
        AtomicInteger wins = new AtomicInteger();
        AtomicInteger losses = new AtomicInteger();
        AtomicInteger draws = new AtomicInteger();
        AtomicInteger blocks_violations = new AtomicInteger();
        AtomicInteger misses = new AtomicInteger();
        AtomicInteger blocks = new AtomicInteger();
        AtomicInteger forks = new AtomicInteger();
        LinkedList<Integer> threads = new LinkedList();
        double[] block_violations = new double[this.threads];
        double[] win_violations = new double[this.threads];
        double[] fork_violations = new double[this.threads];
        double[] block_good = new double[this.threads];
        double[] win_good = new double[this.threads];
        double[] fork_good = new double[this.threads];
        double[] requests = new double[this.threads];
        for (int i = 0; i < 50; i++) {
            InMemoryEventLoggingListener logger = new InMemoryEventLoggingListener();
            BProgramRunner brunner = new BProgramRunner(BProgramFactory());
            brunner.addListener(logger);
            brunner.run();
            List<BEvent> events = logger.getEvents();
            String line = "Generation" + gen + "_Game" + i + ": ";
            String extra = "";
            for (BEvent ev : events) {
                switch (ev.name) {
                    case "OWin":
                        wins.getAndIncrement();
                        for(Integer index : threads){
                            win_good[index]++;
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
                        for(Integer index : threads){
                            block_violations[index]++;
                        }
                        break;
                    case "WIN_VIOLATION":
                        misses.getAndIncrement();
                        for(Integer index : threads){
                            win_violations[index]++;
                        }
                        break;
                    case "FORK_VIOLATION":
                        forks.getAndIncrement();
                        for(Integer index : threads){
                            fork_violations[index]++;
                        }
                        break;
                    case "FORK":
                        for(Integer index : threads){
                            fork_good[index]++;
                        }
                        break;
                    case "BLOCK":
                        blocks.getAndIncrement();
                        for(Integer index : threads){
                            block_good[index]++;
                        }
                        break;
                    case "X":
                        if(id == 1) {
                            Map<String, Number> data = (Map<String, Number>) ev.maybeData;
                            extra = "(" + data.get("row").intValue() + "," + data.get("col").intValue() + ")";
                        }
                        break;
                    case "O":
                        threads.clear();
                        if(id == 1) {
                            Map<String, Number> data2 = (Map<String, Number>) ev.maybeData;
                            extra = "(" + data2.get("row").intValue() + "," + data2.get("col").intValue() + ")";
                        }
                        break;
                    default:
                        int index = Integer.parseInt(ev.name.substring(6));
                        //int index = Character.getNumericValue(ev.name.charAt(6));
                        threads.add(index);
                        requests[index]++;
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
        double deadlocks = 50 - wins.get() - losses.get() - draws.get();
        double[] results = new double[]{wins.get(), losses.get(), draws.get(), blocks_violations.get(), misses.get(), blocks.get(), deadlocks, forks.get() };
        return new double[][]{results, block_violations, win_violations, fork_violations, block_good, win_good, fork_good, requests};

    }
}
