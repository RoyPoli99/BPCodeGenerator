//import il.ac.bgu.cs.bp.bpjs.execution.BProgramRunner;
import il.ac.bgu.cs.bp.bpjs.analysis.DfsBProgramVerifier;
import il.ac.bgu.cs.bp.bpjs.analysis.ExecutionTraceInspection;
import il.ac.bgu.cs.bp.bpjs.analysis.VerificationResult;
import il.ac.bgu.cs.bp.bpjs.analysis.listeners.PrintDfsVerifierListener;
import il.ac.bgu.cs.bp.bpjs.execution.listeners.InMemoryEventLoggingListener;
import il.ac.bgu.cs.bp.bpjs.model.BEvent;
import il.ac.bgu.cs.bp.bpjs.model.BProgram;
import il.ac.bgu.cs.bp.bpjs.model.StringBProgram;
import io.grpc.stub.StreamObserver;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.List;
import java.util.Scanner;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Future;

public class EvaluationServiceImpl extends EvaluationServiceGrpc.EvaluationServiceImplBase{

    private static String rand_player;
    private static String opt_player;
    private ExecutorService es;
    static {
        try {
            rand_player = new Scanner(new File("src/main/resources/BPJSTicTacToeRand.js")).useDelimiter("\\Z").next();
            opt_player = new Scanner(new File("src/main/resources/BPJSTicTacToeOpt.js")).useDelimiter("\\Z").next();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }

    public EvaluationServiceImpl(ExecutorService es){
        super();
        this.es = es;
    }


    @Override
    public void evaluate(Bp.EvaluationRequest request, StreamObserver<Bp.EvaluationResponse> responseObserver) {
        String code = request.getIndividual().getCode().getCode();
        int gen = request.getIndividual().getGeneration();
        int[] res = run_games(code, gen);
        System.out.println("here");
        Bp.EvaluationResponse response = Bp.EvaluationResponse.newBuilder()
                .setDraws(res[1])
                .setWins(res[0])
                .build();
        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }

    private int[] run_games(String code, int generation){
        String[] bthreads = code.split("\n");
        String player;
        if(generation >= 100)
            player = opt_player;
        else
            player = rand_player;
        String b_program = add_bthreads(bthreads, player);
        int wins = 0;
        int draws = 0;
        BProgram bp = new StringBProgram(b_program);
        DfsBProgramVerifier vrf = new DfsBProgramVerifier();
        VerificationResult res;
        try {
            res = vrf.verify(bp);
            int x = 3;
        } catch (Exception e) {
            e.printStackTrace();
        }
        //TODO: run verify once? or play multiple games and look for violations? maybe both?
        /* The following code runs the games, above code is verification
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
        }*/
        return new int[]{wins, draws};
    }

    private String add_bthreads(String[] btheads, String player_text){
        String curr = player_text;
        for(int i = 0; i <= 9; i++)
            curr = curr.replaceAll("bThread" + i, btheads[i]);
        return curr;
    }
}
