import il.ac.bgu.cs.bp.bpjs.execution.listeners.InMemoryEventLoggingListener;
import il.ac.bgu.cs.bp.bpjs.model.BEvent;

import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class RunnerEvaluator extends Evaluator {
  private static ExecutorService es = Executors.newCachedThreadPool();

  public RunnerEvaluator(String code, int gen, int id) {
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
        .build();
  }

  private double[] run_games() {
    InMemoryEventLoggingListener[] loggers = new InMemoryEventLoggingListener[50];
    Future<?>[] futures = new Future[50];
    for (int i = 0; i < 50; i++) {
      loggers[i] = new InMemoryEventLoggingListener();
      BProgramRunner brunner = new BProgramRunner(bprog, es);
      brunner.addListener(loggers[i]);
      futures[i] = es.submit(brunner);
    }
    int wins = 0, losses = 0, draws = 0, blocks = 0, misses = 0;
    for (int i = 0; i < 50; i++) {
      try {
        futures[i].get();
      } catch (Exception e) {
        e.printStackTrace();
      }
      List<BEvent> events = loggers[i].getEvents();
      for (BEvent ev : events) {
        switch (ev.name) {
          case "OWin":
            wins++;
            break;
          case "XWin":
            losses++;
            break;
          case "Draw":
            draws++;
            break;
          case "BLOCK_VIOLATION":
            blocks++;
            break;
          case "WIN_VIOLATION":
            misses++;
        }
      }
    }
    double traceNum = 50;
    return new double[]{wins / traceNum, losses / traceNum, draws / traceNum, blocks / traceNum, misses / traceNum};

  }
}
