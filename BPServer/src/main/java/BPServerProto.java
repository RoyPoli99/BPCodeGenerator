import io.grpc.*;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class BPServerProto {

    public static void main(String[] args) throws Exception {
        ExecutorService es = Executors.newFixedThreadPool(10);
        //ExecutorService es = Executors.newFixedThreadPool(Integer.parseInt(args[0]));
        Server server = ServerBuilder.forPort(8080)
                .addService(new EvaluationServiceImpl(es))
                .build();
        server.start();
        System.out.println("Server started");
        server.awaitTermination();
    }

}
