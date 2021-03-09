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

    public RunnerEvaluatorOrg(String code, int gen, int id) {
        super(code, gen, id, gen > 100 ? "opt" : "rand");
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
                .build();
    }

    private double[] run_games() {
        //InMemoryEventLoggingListener[] loggers = new InMemoryEventLoggingListener[50];
    /*Future<?>[] futures = new Future[50];
    for (int i = 0; i < 50; i++) {
      loggers[i] = new InMemoryEventLoggingListener();
      EvoBP.BProgramRunner brunner = new EvoBP.BProgramRunner(bprog, es);
      brunner.addListener(loggers[i]);
      futures[i] = es.submit(brunner);
    }*/
        AtomicInteger wins = new AtomicInteger();
        AtomicInteger losses = new AtomicInteger();
        AtomicInteger draws = new AtomicInteger();
        AtomicInteger blocks = new AtomicInteger();
        AtomicInteger misses = new AtomicInteger();
        Set<List<Integer>> numbers = new HashSet<>();
        Random rand = new Random();
//        for (int i = 0; i < 50; i++) {
//            List<Integer> l = new LinkedList<>();
//            for (int j = 0; j < 4; j++) {
//                l.add(rand.nextInt(9-j*2));
//            }
//            numbers.add(l);
//        }
//        numbers.forEach(l -> {
      /*
      try {
        while(!futures[i].isDone()) {
          Thread.sleep(1000);
        }
      } catch (Exception e) {
        e.printStackTrace();
      }*/
        for (int i = 0; i < 50; i++) {
            InMemoryEventLoggingListener logger = new InMemoryEventLoggingListener();
            BProgramRunner brunner = new BProgramRunner(BProgramFactory());
            //brunner.addListener(new EvoBP.RunnerXPlayer(l));
            brunner.addListener(logger);
            brunner.run();
            List<BEvent> events = logger.getEvents();
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
                }
            }
        }
        //});
        double traceNum = 50;
        return new double[]{wins.get() / traceNum, losses.get() / traceNum, draws.get() / traceNum, blocks.get() / traceNum, misses.get() / traceNum};

    }
}
