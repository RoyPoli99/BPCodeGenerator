package evoBP;

import il.ac.bgu.cs.bp.bpjs.execution.BProgramRunner;
import il.ac.bgu.cs.bp.bpjs.execution.listeners.PrintBProgramRunnerListener;
import il.ac.bgu.cs.bp.bpjs.model.BProgram;
import il.ac.bgu.cs.bp.bpjs.model.ResourceBProgram;
import il.ac.bgu.cs.bp.bpjs.model.eventselection.PrioritizedBSyncEventSelectionStrategy;

public class Runner {
  public static void main(String[] args) throws InterruptedException {
    // This will load the program file  <Project>/src/main/resources/HelloBPjsWorld.js
    final BProgram bprog = new ResourceBProgram("TTT.js");
    var prio = new PrioritizedBSyncEventSelectionStrategy();
    prio.setDefaultPriority(0);
    bprog.setEventSelectionStrategy(prio);

    BProgramRunner rnr = new BProgramRunner(bprog);
    // Print program events to the console
    rnr.addListener( new PrintBProgramRunnerListener() );

    // go!
    rnr.run();
  }
}
