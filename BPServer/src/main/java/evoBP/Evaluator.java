package evoBP;

import il.ac.bgu.cs.bp.bpjs.model.BProgram;
import il.ac.bgu.cs.bp.bpjs.model.StringBProgram;
import il.ac.bgu.cs.bp.bpjs.model.eventselection.PrioritizedBSyncEventSelectionStrategy;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.concurrent.Callable;

public abstract class Evaluator implements Callable<Bp.EvaluationResponse> {

    private static String first_x;
    private static String first_o;
    private static String first_opt_x;
    private static String first_opt_o;
    static {
        try {
            first_x = new Scanner(new File("resources/BPJSTicTacToeFirstX.js")).useDelimiter("\\Z").next();
            first_o = new Scanner(new File("resources/BPJSTicTacToeFirstO.js")).useDelimiter("\\Z").next();
            first_opt_x = new Scanner(new File("resources/BPJSTicTacToeOptFirstX.js")).useDelimiter("\\Z").next();
            first_opt_o = new Scanner(new File("resources/BPJSTicTacToeOptFirstO.js")).useDelimiter("\\Z").next();
        } catch (FileNotFoundException e) {
            try{
                first_x = new Scanner(new File("src/main/resources/BPJSTicTacToeFirstX.js")).useDelimiter("\\Z").next();
                first_o = new Scanner(new File("src/main/resources/BPJSTicTacToeFirstO.js")).useDelimiter("\\Z").next();
                first_opt_x = new Scanner(new File("src/main/resources/BPJSTicTacToeOptFirstX.js")).useDelimiter("\\Z").next();
                first_opt_o = new Scanner(new File("src/main/resources/BPJSTicTacToeOptFirstO.js")).useDelimiter("\\Z").next();
            } catch (FileNotFoundException e2) {
                e.printStackTrace();
            }
        }
    }

    protected final int gen;
    protected final int id;
    protected final String b_program_first_x;
    protected final String b_program_first_o;
    protected final String b_program_opt_first_x;
    protected final String b_program_opt_first_o;


    protected Evaluator(String code, int gen, int id, String playerType){
        super();
        this.id = id;
        this.gen = gen;
        //String[] bthreads = code.split("\n");
        String player;
        //if(playerType.equals("opt"))
        //    player = opt_player;
        //else
        // player = rand_player;
        // b_program = add_bthreads(code, player);
        b_program_first_x = add_bthreads(code, first_x);
        b_program_first_o = add_bthreads(code, first_o);
        b_program_opt_first_x = add_bthreads(code, first_opt_x);
        b_program_opt_first_o = add_bthreads(code, first_opt_o);
        /*
        bprog = new StringBProgram(b_program);
        var prio = new PrioritizedBSyncEventSelectionStrategy();
        prio.setDefaultPriority(0);
        bprog.setEventSelectionStrategy(prio);*/
    }

    protected abstract Bp.EvaluationResponse evaluate();

    @Override
    public final Bp.EvaluationResponse call() {
        //System.out.println("Generation #" + gen + ": Evaluating individual #" + id);
        var res = evaluate();
        //System.out.println("Generation #" + this.gen + ": Completed individual #" + this.id);
        return res;
    }

    private static String add_bthreads(String bthreads, String player_text) {
        int cut_index = bthreads.indexOf("bp.registerBThread(\"O_Player_Other_1\"");
        String curr = player_text;
        //String lines = bthreads.substring(0, cut_index);
        //String others = bthreads.substring(cut_index, bthreads.length());
        //curr = curr.replaceAll("LINE_CODE", lines);
        curr = curr.replaceAll("O_PLAYER_CODE", bthreads);
        return curr;
    }

    protected BProgram BProgramFactory(String player_type){
        BProgram bprog;
        switch(player_type){
            case "rand_x":
                bprog = new StringBProgram(b_program_first_x);
                break;
            case "rand_o":
                bprog = new StringBProgram(b_program_first_o);
                break;
            case "opt_x":
                bprog = new StringBProgram(b_program_opt_first_x);
                break;
            case "opt_o":
                bprog = new StringBProgram(b_program_opt_first_o);
                break;
            default:
                bprog = null;
                break;
        }
        var prio = new PrioritizedBSyncEventSelectionStrategy();
        prio.setDefaultPriority(0);
        bprog.setEventSelectionStrategy(prio);
        return bprog;
    }
}
