import io.grpc.*;

import java.lang.management.ManagementFactory;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class BPServerProto {

    public static void main(String[] args) throws Exception {
        int numOfThreads = ManagementFactory.getThreadMXBean().getThreadCount();
        System.out.println("Number of threads="+numOfThreads);
        ExecutorService es = Executors.newFixedThreadPool(numOfThreads);
        //ExecutorService es = Executors.newFixedThreadPool(Integer.parseInt(args[0]));
        Server server = ServerBuilder.forPort(50051)
                .addService(new EvaluationServiceImpl(es))
                .build();
        server.start();
        System.out.println("Server started");
        server.awaitTermination();
    }

}
