import il.ac.bgu.cs.bp.bpjs.analysis.DfsBProgramVerifier;
import il.ac.bgu.cs.bp.bpjs.analysis.listeners.PrintDfsVerifierListener;
import il.ac.bgu.cs.bp.bpjs.model.BEvent;
import il.ac.bgu.cs.bp.bpjs.model.BProgram;
import il.ac.bgu.cs.bp.bpjs.model.StringBProgram;
import io.grpc.stub.StreamObserver;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Collection;
import java.util.List;
import java.util.Scanner;
import java.util.concurrent.ExecutorService;

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
        System.out.println("Generation #" + gen + ": Evaluating individual #" + request.getIndividual().getId());
        double[] res = run_games(code, gen);
        Bp.EvaluationResponse response = Bp.EvaluationResponse.newBuilder()
                .setWins(res[0])
                .setLosses(res[1])
                .setDraws(res[2])
                .setBlocks(res[3])
                .setMisses(res[4])
                .build();
        System.out.println("Generation #" + gen + ": Completed individual #" + request.getIndividual().getId());
        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }


    private double[] run_games(String code, int generation){
        String[] bthreads = code.split("\n");
        String player;
        if(generation >= 200)
            player = opt_player;
        else
            player = rand_player;
        String b_program = add_bthreads(bthreads, player);
        //int wins = 0;
        //int draws = 0;

        BProgram bp = new StringBProgram(b_program);
        return verify(bp);

        /*
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
        }*/
        // return new int[]{wins, draws};
    }

    private double[] verify(BProgram bprog){
        bprog.setEventSelectionStrategy(new PrioritizedBSyncEventSelectionStrategy());
        GenerateAllTracesInspection inspector = new GenerateAllTracesInspection();
        DfsBProgramVerifier vfr = new DfsBProgramVerifier();
        vfr.addInspection(inspector);
        vfr.setProgressListener(new PrintDfsVerifierListener());
        vfr.setIterationCountGap(100);
        vfr.setMaxTraceLength(10);
        try {
            vfr.verify(bprog);
            System.out.println("finished verification, starting traces generation");
            Collection<List<BEvent>> traces = inspector.calculateAllTraces();
            int wins = 0, losses = 0, draws = 0, blocks = 0, misses = 0;
            for(List<BEvent> trace : traces){
                String lastEvent = trace.get(trace.size() - 1).name;
                for(BEvent ev : trace){
                    switch(ev.name){
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
            double traceNum = traces.size();
            return new double[]{wins / traceNum, losses / traceNum, draws / traceNum, blocks / traceNum, misses / traceNum};
        } catch (Exception e) {
            e.printStackTrace();
            return new double[]{0, 0, 0, 0, 0};
        }
    }

    private String add_bthreads(String[] btheads, String player_text){
        String curr = player_text;
        for(int i = 0; i <= 9; i++)
            curr = curr.replaceAll("bThread" + i, btheads[i]);
        return curr;
    }
}
