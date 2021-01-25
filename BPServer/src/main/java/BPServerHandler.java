import il.ac.bgu.cs.bp.bpjs.execution.BProgramRunner;
import il.ac.bgu.cs.bp.bpjs.execution.listeners.InMemoryEventLoggingListener;
import il.ac.bgu.cs.bp.bpjs.execution.listeners.PrintBProgramRunnerListener;
import il.ac.bgu.cs.bp.bpjs.model.BEvent;
import il.ac.bgu.cs.bp.bpjs.model.BProgram;
import il.ac.bgu.cs.bp.bpjs.model.StringBProgram;
import io.netty.channel.*;
import io.netty.channel.group.ChannelGroup;
import io.netty.channel.group.DefaultChannelGroup;
import io.netty.util.concurrent.GlobalEventExecutor;
import org.mozilla.javascript.Scriptable;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.LinkedList;
import java.util.List;
import java.util.Scanner;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class BPServerHandler extends SimpleChannelInboundHandler<String> {

    private static final ChannelGroup channels = new DefaultChannelGroup(GlobalEventExecutor.INSTANCE);
    private String rand_player;
    private String opt_player;
    private String curr_msg = "";

    {
        try {
            rand_player = new Scanner(new File("src/main/resources/BPJSTicTacToeRand.js")).useDelimiter("\\Z").next();
            opt_player = new Scanner(new File("src/main/resources/BPJSTicTacToeOpt.js")).useDelimiter("\\Z").next();
        } catch (FileNotFoundException e) {
            try {
                rand_player = new Scanner(new File("resources/BPJSTicTacToeRand.js")).useDelimiter("\\Z").next();
                opt_player = new Scanner(new File("resources/BPJSTicTacToeOpt.js")).useDelimiter("\\Z").next();
            } catch (FileNotFoundException fileNotFoundException) {
                fileNotFoundException.printStackTrace();
            }
        }
    }

    @Override
    protected void channelRead0(ChannelHandlerContext channelHandlerContext, String message) throws Exception {
        Channel incoming = channelHandlerContext.channel();
        //Bp.BProgram.Builder builder = Bp.BProgram.newBuilder();
        //Bp.BProgram msg = Bp.BProgram.parseFrom(message.getBytes());
        curr_msg += message;
        String response = "";
        if(curr_msg.contains("END")){
            //System.out.println("HERE");
            double result = run_games(curr_msg);
            response = String.valueOf(result);
            channelHandlerContext.writeAndFlush(response).addListener(ChannelFutureListener.CLOSE);
        }
        if(curr_msg.contains("STOP_SERVER")){
            System.exit(0);
        }
    }

    private String add_bthreads(String[] btheads, String player_text){
        String curr = player_text;
        for(int i = 0; i <= 9; i++)
            curr = curr.replaceAll("bThread" + i, btheads[i]);
        return curr;
    }

    private String read_file(String path){
        String content = "";

        try
        {
            content = Files.readString(Paths.get(path), StandardCharsets.US_ASCII);
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }

        return content;
    }

    private double run_games(String code){
        String[] msg = code.split("START");
        String[] clear = msg[1].split("END");
        String[] bthreads = clear[0].split("\n");
        String player;
        if(clear[1].equals("RAND"))
            player = opt_player;
        else
            player = opt_player;
        String b_program = add_bthreads(bthreads, player);
        double score = 0;
        //ExecutorService executorService = Executors.newFixedThreadPool(30);
        //List<Future<List<BEvent>>> futures = new LinkedList<>();
        for(int i=0; i<30; i++) {
            BProgram bp = new StringBProgram(b_program);
            InMemoryEventLoggingListener logger = new InMemoryEventLoggingListener();
            BProgramRunner brunner = new BProgramRunner(bp);
            brunner.addListener(logger);
            //Future<List<BEvent>> future = executorService.submit(() -> {
            //    brunner.run();
            //    return logger.getEvents();
            //});
            //futures.add(future);

             //Thread t = new Thread(brunner);
             //t.start();

             brunner.run();
             List<BEvent> events = logger.getEvents();
             String result = (events.get(events.size() - 1)).name;
             if(result.equals("Draw") || result.equals("OWin")) {
                 score += 1;
             }
        }
        /*
        for(int i=0; i<futures.size(); i++){
            try {
                score += getDrawScore(futures.get(i).get());
            } catch (InterruptedException | ExecutionException e) {
                e.printStackTrace();
            }
        }*/

        return score;
    }

    private double getDrawScore(List<BEvent> events){
        String result = (events.get(events.size() - 1)).name;
        if(result.equals("Draw") || result.equals("OWin")) {
            return 1;
        }
        return 0;
    }
}
