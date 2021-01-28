import il.ac.bgu.cs.bp.bpjs.analysis.DfsBProgramVerifier;
import il.ac.bgu.cs.bp.bpjs.analysis.listeners.PrintDfsVerifierListener;
import il.ac.bgu.cs.bp.bpjs.model.BEvent;
import il.ac.bgu.cs.bp.bpjs.model.BProgram;
import il.ac.bgu.cs.bp.bpjs.model.ResourceBProgram;

import java.util.Collection;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import static java.util.stream.Collectors.joining;


public class Verifier {
  public static void main(String[] args) throws InterruptedException {
    final BProgram bprog = new ResourceBProgram("TTT.js");
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
      Collection<List<Cell>> tracesCells = traces.stream().map(l -> l.stream().map(Cell::new).collect(Collectors.toList())).sorted(new TraceComperator()).collect(Collectors.toList());
      String tracesS = tracesCells.toString();
      System.out.println(tracesCells);
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private static class TraceComperator implements Comparator<List<Cell>> {
    @Override
    public int compare(List<Cell> o1, List<Cell> o2) {
      for(int i = 0; i < o1.size(); i++) {
        if(i == o2.size()) return 1;
        int c = o1.get(i).compareTo(o2.get(i));
        if(c != 0) return c;
      }
      if(o1.size() < o2.size()) return -1;
      return 0;
//      return o1.stream().map(Cell::toString).collect(joining(",")).compareTo(
//          o2.stream().map(Cell::toString).collect(joining(","))
//      );
    }
  }

  public static class Cell implements Comparable<Cell>{
    public final int x;
    public final int y;
    public final char val;

    public Cell(BEvent e) {
      this((Map)e.maybeData, e.name.charAt(0));
    }

    public Cell(Map data, char val) {
      this((int)data.get("row"), (int)data.get("col"), val);
    }

    public Cell(int x, int y, char val) {
      this.x = x;
      this.y = y;
      this.val = val;
    }

    @Override
    public String toString() {
      return val + "("+x+","+y+")";
    }

    @Override
    public int compareTo(Cell o) {
      if(x<o.x) return -1;
      if(x==o.x) return y - o.y;
      return 1;
    }
  }
}


