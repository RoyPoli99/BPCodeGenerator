import il.ac.bgu.cs.bp.bpjs.model.eventselection.PrioritizedBSyncEventSelectionStrategy;

public class RunnerEvaluator extends Evaluator {
    public RunnerEvaluator(String code, int gen, int id) {
        super(code,gen,id);
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

    private double[] run_games(){
        var prio =new PrioritizedBSyncEventSelectionStrategy();
        prio.setDefaultPriority(0);
        bprog.setEventSelectionStrategy(prio);
        return null;
    }
}
