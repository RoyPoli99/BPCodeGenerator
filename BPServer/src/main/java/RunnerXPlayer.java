import il.ac.bgu.cs.bp.bpjs.execution.BProgramRunner;
import il.ac.bgu.cs.bp.bpjs.execution.listeners.BProgramRunnerListenerAdapter;
import il.ac.bgu.cs.bp.bpjs.execution.listeners.InMemoryEventLoggingListener;
import il.ac.bgu.cs.bp.bpjs.model.BEvent;
import il.ac.bgu.cs.bp.bpjs.model.BProgram;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class RunnerXPlayer extends BProgramRunnerListenerAdapter {
  private final List<Integer> numbers;
  private char[][] board = new char[3][3];

  public RunnerXPlayer(List<Integer> list) {
    this.numbers = list;
  }

  @Override
  public void eventSelected(BProgram bp, BEvent e) {
    if(e.name.equals("X")||e.name.equals("O")) {
      Map<String, Number> data = (Map<String, Number>) e.maybeData;
      System.out.println("prev char is - " + board[data.get("row").intValue()][data.get("col").intValue()]);
      board[data.get("row").intValue()][data.get("col").intValue()] = e.name.charAt(0);
    }
    if(e.name.equals("O")||e.name.equals("Game_Start")) {
      int nextNumber = numbers.remove(0);
      int[] position = get_position(nextNumber);
      double curr_row = position[0], curr_col = position[1];
      bp.enqueueExternalEvent(new BEvent("X", Map.of("row", curr_row, "col", curr_col)));
    }
  }

  private int[] get_position(int next){
    int counter = next;
    for(int i = 0; i < 3; i++){
      for(int j = 0; j < 3; j++){
        if(board[i][j] == 0){
          if(counter == 0){
            return new int[]{i, j};
          }
          else{
            counter--;
          }
        }
      }
    }
    return new int[0];
  }
}
