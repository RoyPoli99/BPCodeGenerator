import il.ac.bgu.cs.bp.bpjs.analysis.ExecutionTrace;
import il.ac.bgu.cs.bp.bpjs.analysis.ExecutionTraceInspection;
import il.ac.bgu.cs.bp.bpjs.analysis.violations.Violation;
import il.ac.bgu.cs.bp.bpjs.model.BEvent;
import il.ac.bgu.cs.bp.bpjs.model.BProgramSyncSnapshot;

import java.util.*;
import java.util.stream.Collectors;

public class GenerateAllTracesInspection implements ExecutionTraceInspection {
  /**
   * Maps <sourceNodeId, <targetNodeId, eventFromSourceToTarget>>
   */
  private final Map<BProgramSyncSnapshot, Map<BProgramSyncSnapshot, BEvent>> graph = new TreeMap<>();
  private BProgramSyncSnapshot startNode;

  @Override
  public String title() {
    return "GenerateAllTracesInspector";
  }

  @Override
  public Optional<Violation> inspectTrace(ExecutionTrace aTrace) {
    int stateCount = aTrace.getStateCount();
    var lastNode = aTrace.getNodes().get(stateCount - 1);
    if (stateCount == 1) {
      startNode = aTrace.getNodes().get(0).getState();
    } else {
      var src = aTrace.getNodes().get(stateCount - 2);
      Map<BProgramSyncSnapshot, BEvent> srcNode = graph.computeIfAbsent(src.getState(), k -> new TreeMap<>());
      srcNode.put(lastNode.getState(), src.getEvent().get());
    }
    return Optional.empty();
  }

  public Collection<List<BEvent>> calculateAllTraces() {
    return dfsFrom(startNode, new ArrayDeque<>(), new ArrayDeque<>());
  }

  private Collection<List<BEvent>> dfsFrom(BProgramSyncSnapshot id, ArrayDeque<BProgramSyncSnapshot> nodeStack, ArrayDeque<BEvent> eventStack) {
    Map<BProgramSyncSnapshot, BEvent> outbounds = graph.get(id);
    nodeStack.push(id);
    if (outbounds == null || outbounds.isEmpty()) {
      nodeStack.pop();
      return new ArrayList<>() {{
        add(new ArrayList<>(eventStack));
      }};
    } else {
      Collection<List<BEvent>> res = outbounds.entrySet().stream()
          .filter(e -> !nodeStack.contains(e.getKey()))
          .map(e -> {
            eventStack.push(e.getValue());
            Collection<List<BEvent>> innerDfs = dfsFrom(e.getKey(),nodeStack,eventStack);
            eventStack.pop();
            return innerDfs;
          })
          .flatMap(Collection::stream)
          .collect(Collectors.toList());
      nodeStack.pop();
      return res;
    }
  }


}