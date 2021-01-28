import il.ac.bgu.cs.bp.bpjs.execution.BProgramRunner;
import il.ac.bgu.cs.bp.bpjs.execution.listeners.PrintBProgramRunnerListener;
import il.ac.bgu.cs.bp.bpjs.model.BProgram;
import il.ac.bgu.cs.bp.bpjs.model.ResourceBProgram;

public class Runner {
  public static void main(String[] args) throws InterruptedException {
    // This will load the program file  <Project>/src/main/resources/HelloBPjsWorld.js
    final BProgram bprog = new ResourceBProgram("TTT.js");
    bprog.setEventSelectionStrategy(new PrioritizedBSyncEventSelectionStrategy());

    BProgramRunner rnr = new BProgramRunner(bprog);
    // Print program events to the console
    rnr.addListener( new PrintBProgramRunnerListener() );

    // go!
    rnr.run();
  }
}
