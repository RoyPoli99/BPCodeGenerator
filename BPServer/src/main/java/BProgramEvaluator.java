import il.ac.bgu.cs.bp.bpjs.execution.BProgramRunner;
import il.ac.bgu.cs.bp.bpjs.execution.listeners.PrintBProgramRunnerListener;
import il.ac.bgu.cs.bp.bpjs.model.BProgram;
import io.netty.channel.ChannelFutureListener;

public abstract class BProgramEvaluator {
    private final BProgram bp;

    protected  BProgramEvaluator(BProgram bp) {
        this.bp=bp;
    }

    public EvaluationResult evaluate() {
        BProgramRunner brunner = new BProgramRunner(bp);
        PrintBProgramRunnerListener printer = new PrintBProgramRunnerListener();
        brunner.addListener(printer);
        brunner.run();

        return new EvaluationResult();
    }

    protected abstract EvaluationResult innerEvaluate();
}
