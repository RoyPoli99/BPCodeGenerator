import il.ac.bgu.cs.bp.bpjs.analysis.DfsBProgramVerifier;
import io.grpc.stub.StreamObserver;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.FutureTask;

public class EvaluationServiceImpl extends EvaluationServiceGrpc.EvaluationServiceImplBase{
    ExecutorService es;

    public EvaluationServiceImpl(ExecutorService es){
        super();
        this.es = es;
    }


    @Override
    public void evaluate(Bp.EvaluationRequest request, StreamObserver<Bp.EvaluationResponse> responseObserver) {
        String code = request.getIndividual().getCode().getCode();
        int gen = request.getIndividual().getGeneration();
        int id = request.getIndividual().getId();

        var evaluator = new VerificationEvaluator(es, code, gen, id);
        var task = new FutureTask<>(evaluator);
        es.submit(task);

        responseObserver.onNext(response); //take future
        responseObserver.onCompleted();
    }
}
