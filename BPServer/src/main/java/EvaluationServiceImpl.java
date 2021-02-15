import io.grpc.stub.StreamObserver;

import java.util.concurrent.ExecutorService;

public class EvaluationServiceImpl extends EvaluationServiceGrpc.EvaluationServiceImplBase {
  public EvaluationServiceImpl() {
    super();
  }


  @Override
  public void evaluate(Bp.EvaluationRequest request, StreamObserver<Bp.EvaluationResponse> responseObserver) {
    String code = request.getIndividual().getCode().getCode();
    int gen = request.getIndividual().getGeneration();
    int id = request.getIndividual().getId();
    var evaluator = new VerificationEvaluator(code, gen, id);
    responseObserver.onNext(evaluator.call()); //take future
    responseObserver.onCompleted();
  }
}
