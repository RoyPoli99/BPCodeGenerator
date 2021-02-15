import il.ac.bgu.cs.bp.bpjs.analysis.DfsBProgramVerifier;
import il.ac.bgu.cs.bp.bpjs.model.BEvent;
import il.ac.bgu.cs.bp.bpjs.model.BProgram;
import il.ac.bgu.cs.bp.bpjs.model.StringBProgram;
import il.ac.bgu.cs.bp.bpjs.model.eventselection.PrioritizedBSyncEventSelectionStrategy;
import io.grpc.stub.StreamObserver;

import java.util.Collection;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

public class VerificationEvaluator extends Evaluator {
    public VerificationEvaluator(ExecutorService es, String code, int gen, int id) {
        super(es, code,gen,id);
    }

    @Override
    protected Bp.EvaluationResponse evaluate() {
        double[] res = verify();
        return Bp.EvaluationResponse.newBuilder()
                .setWins(res[0])
                .setLosses(res[1])
                .setDraws(res[2])
                .setBlocks(res[3])
                .setMisses(res[4])
                .build();
    }

    private double[] verify(){
        var prio = new PrioritizedBSyncEventSelectionStrategy();
        prio.setDefaultPriority(0);
        bprog.setEventSelectionStrategy(prio);
        GenerateAllTracesInspection inspector = new GenerateAllTracesInspection();
        DfsBProgramVerifier vfr = new DfsBProgramVerifier();
        vfr.addInspection(inspector);
        //vfr.setProgressListener(new PrintDfsVerifierListener());
        vfr.setIterationCountGap(100);
        vfr.setMaxTraceLength(10);
        try {
            vfr.verify(bprog);
            //System.out.println("finished verification, starting traces generation");
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
}
