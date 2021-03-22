package evoBP;

import il.ac.bgu.cs.bp.bpjs.execution.listeners.InMemoryEventLoggingListener;
import il.ac.bgu.cs.bp.bpjs.model.BEvent;
import il.ac.bgu.cs.bp.bpjs.execution.BProgramRunner;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

public class RunnerEvaluatorOrg extends Evaluator {
    private static ExecutorService es = Executors.newCachedThreadPool();

    public RunnerEvaluatorOrg(String code, int gen, int id) {
        super(code, gen, id, gen > 200 ? "opt" : "rand");
    }

    @Override
    protected Bp.EvaluationResponse evaluate() {
        double[] res = run_games();
        return Bp.EvaluationResponse.newBuilder()
                .setWins(res[0])
                .setLosses(res[1])
                .setDraws(res[2])
                .setBlocks(res[3])
                .setMisses(res[4])
                .setLength(res[5])
                .build();
    }

    private double[] run_games() {
        AtomicInteger wins = new AtomicInteger();
        AtomicInteger losses = new AtomicInteger();
        AtomicInteger draws = new AtomicInteger();
        AtomicInteger blocks = new AtomicInteger();
        AtomicInteger misses = new AtomicInteger();
        AtomicInteger lengths = new AtomicInteger();
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
                        break;
                    case "XWin":
                        losses.getAndIncrement();
                        break;
                    case "Draw":
                        draws.getAndIncrement();
                        break;
                    case "BLOCK_VIOLATION":
                        blocks.getAndIncrement();
                        break;
                    case "WIN_VIOLATION":
                        misses.getAndIncrement();
                        break;
                    case "X":
                        lengths.getAndIncrement();
                        if(id == 1) {
                            Map<String, Number> data = (Map<String, Number>) ev.maybeData;
                            extra = "(" + data.get("row").intValue() + "," + data.get("col").intValue() + ")";
                        }
                        break;
                    case "O":
                        lengths.getAndIncrement();
                        if(id == 1) {
                            Map<String, Number> data2 = (Map<String, Number>) ev.maybeData;
                            extra = "(" + data2.get("row").intValue() + "," + data2.get("col").intValue() + ")";
                        }
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
        double traceNum = 50;
        return new double[]{wins.get() / traceNum, losses.get() / traceNum, draws.get() / traceNum, blocks.get() / traceNum, misses.get() / traceNum, lengths.get() / traceNum};

    }
}
