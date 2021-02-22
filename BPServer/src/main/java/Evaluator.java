import il.ac.bgu.cs.bp.bpjs.model.BProgram;
import il.ac.bgu.cs.bp.bpjs.model.StringBProgram;
import il.ac.bgu.cs.bp.bpjs.model.eventselection.PrioritizedBSyncEventSelectionStrategy;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.concurrent.Callable;

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

    protected final int gen;
    protected final int id;
    protected final BProgram bprog;


    protected Evaluator(String code, int gen, int id, String playerType){
        super();
        this.id = id;
        this.gen = gen;
        String[] bthreads = code.split("\n");
        String player;
        if(playerType.equals("opt"))
            player = opt_player;
        else
            player = rand_player;
        String b_program = add_bthreads(bthreads, player);
        bprog = new StringBProgram(b_program);
        var prio = new PrioritizedBSyncEventSelectionStrategy();
        prio.setDefaultPriority(0);
        bprog.setEventSelectionStrategy(prio);
    }

    protected abstract Bp.EvaluationResponse evaluate();

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
