package evoBP;

import il.ac.bgu.cs.bp.bpjs.model.BEvent;

import java.util.Objects;

public class Move extends BEvent {
    public final int row;
    public final int col;

    public Move(int i, int j, String type) {
        super(type);
        row = i;
        col = j;
    }

    @Override
    public boolean equals(Object obj) {
        if(!(obj instanceof Move)) return false;
        Move m = (Move) obj;
        return Objects.equals(row, m.row) && Objects.equals(name, m.name) && Objects.equals(col, m.col) ;
    }

    @Override
    public int hashCode() {
        return Objects.hash(name,row,col);
    }
}
