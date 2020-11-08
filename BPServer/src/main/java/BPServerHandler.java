import il.ac.bgu.cs.bp.bpjs.execution.BProgramRunner;
import il.ac.bgu.cs.bp.bpjs.execution.listeners.PrintBProgramRunnerListener;
import il.ac.bgu.cs.bp.bpjs.model.BProgram;
import io.netty.channel.*;
import io.netty.channel.group.ChannelGroup;
import io.netty.channel.group.DefaultChannelGroup;
import io.netty.util.concurrent.GlobalEventExecutor;
import org.mozilla.javascript.Scriptable;

public class BPServerHandler extends SimpleChannelInboundHandler<String> {

    private static final ChannelGroup channels = new DefaultChannelGroup(GlobalEventExecutor.INSTANCE);


    @Override
    protected void channelRead0(ChannelHandlerContext channelHandlerContext, String message) throws Exception {
        Channel incoming = channelHandlerContext.channel();
        BProgram bp = new BProgram() {
            @Override
            protected void setupProgramScope(Scriptable scriptable) {

            }
        };
        String[] msg = message.split("START");

        bp.appendSource(msg[1]);
        BProgramRunner brunner = new BProgramRunner(bp);
        PrintBProgramRunnerListener printer = new PrintBProgramRunnerListener();
        brunner.addListener(printer);
        brunner.run();

        channelHandlerContext.writeAndFlush("DONE" + bp.getName()).addListener(ChannelFutureListener.CLOSE);
    }
}
