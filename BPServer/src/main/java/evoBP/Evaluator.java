package evoBP;

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
            rand_player = new Scanner(new File("resources/RandTicTacToeClean.js")).useDelimiter("\\Z").next();
            //rand_player = new Scanner(new File("resources/BPJSTicTacToe.js")).useDelimiter("\\Z").next();
            opt_player = new Scanner(new File("resources/BPJSTicTacToeOpt.js")).useDelimiter("\\Z").next();
        } catch (FileNotFoundException e) {
            try{
                rand_player = new Scanner(new File("src/main/resources/RandTicTacToeClean.js")).useDelimiter("\\Z").next();
                //rand_player = new Scanner(new File("src/main/resources/BPJSTicTacToe.js")).useDelimiter("\\Z").next();
                opt_player = new Scanner(new File("src/main/resources/BPJSTicTacToeOpt.js")).useDelimiter("\\Z").next();
            } catch (FileNotFoundException e2) {
                e.printStackTrace();
            }
        }
    }

    protected final int gen;
    protected final int id;
    protected final int threads;
    //protected final BProgram bprog;
    protected final String b_program;


    protected Evaluator(String code, int gen, int id, String playerType, int threads){
        super();
        this.id = id;
        this.gen = gen;
        this.threads = threads;
        String player;
        if(playerType.equals("opt"))
            player = opt_player;
        else
            player = rand_player;
        b_program = add_bthreads(code, player);
    }

    protected abstract Bp.EvaluationResponse evaluate();

    @Override
    public final Bp.EvaluationResponse call() {
        var res = evaluate();
        return res;
    }

    private static String add_bthreads(String code, String player_text) {
        String curr = player_text;
        curr = curr.replaceAll("CODE_GOES_HERE", code);
        return curr;
    }

    protected BProgram BProgramFactory(){
        BProgram bprog = new StringBProgram(b_program);
        var prio = new PrioritizedBSyncEventSelectionStrategy();
        prio.setDefaultPriority(0);
        bprog.setEventSelectionStrategy(prio);
        return bprog;
    }
}
