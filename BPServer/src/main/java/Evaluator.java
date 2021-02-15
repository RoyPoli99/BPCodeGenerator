import il.ac.bgu.cs.bp.bpjs.model.BProgram;
import il.ac.bgu.cs.bp.bpjs.model.StringBProgram;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;

public abstract class Evaluator implements Callable<Bp.EvaluationResponse> {

    private static String rand_player;
    private static String opt_player;
    static {
        try {
            rand_player = new Scanner(new File("resources/BPJSTicTacToeRand.js")).useDelimiter("\\Z").next();
            opt_player = new Scanner(new File("resources/BPJSTicTacToeOpt.js")).useDelimiter("\\Z").next();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }

    protected int gen;
    protected int id;
    protected final BProgram bprog;


    protected Evaluator(String code, int gen, int id){
        super();
        String[] bthreads = code.split("\n");
        String player;
        if(gen >= 200)
            player = opt_player;
        else
            player = rand_player;
        String b_program = add_bthreads(bthreads, player);
        bprog = new StringBProgram(b_program);
    }

    protected abstract Bp.EvaluationResponse evaluate();

    /*private double[] run_games(String code, int generation){
        bp.setEventSelectionStrategy(new PrioritizedBSyncEventSelectionStrategy());
        DfsBProgramVerifier vrf = new DfsBProgramVerifier();
        VerificationResult res;
        try {
            res = vrf.verify(bp);
            int x = 3;
        } catch (Exception e) {
            e.printStackTrace();
        }
        */

        /*
        InMemoryEventLoggingListener[] loggers = new InMemoryEventLoggingListener[50];
        Future<?>[] futures = new Future[50];
        for(int i=0; i<50; i++) {
            BProgram bp = new StringBProgram(b_program);
            DfsBProgramVerifier vrf = new DfsBProgramVerifier();
            try {
                VerificationResult res = vrf.verify(bp);
            } catch (Exception e) {
                e.printStackTrace();
            }
            loggers[i] = new InMemoryEventLoggingListener();
            BProgramRunner brunner = new BProgramRunner(bp, this.es);
            brunner.addListener(loggers[i]);
            futures[i] = this.es.submit(brunner);
        }
        for(int i=0; i<50; i++) {
            try {
                futures[i].get();
            } catch (Exception e) {
                e.printStackTrace();
            }
            List<BEvent> events = loggers[i].getEvents();
            String result = (events.get(events.size() - 1)).name;
            if (result.equals("Draw")) {
                draws += 1;
            }
            if (result.equals("OWin")) {
                wins += 1;
            }
        }
        // return new int[]{wins, draws};
    }*/

    @Override
    public final Bp.EvaluationResponse call() {
        System.out.println("Generation #" + gen + ": Evaluating individual #" + id);
        var res = evaluate();
        System.out.println("Generation #" + this.gen + ": Completed individual #" + this.id);
        return res;
    }

    private static String add_bthreads(String[] btheads, String player_text) {
        String curr = player_text;
        for(int i = 0; i <= 9; i++)
            curr = curr.replaceAll("bThread" + i, btheads[i]);
        return curr;
    }
}
