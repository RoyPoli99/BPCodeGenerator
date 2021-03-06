package evoBP;

import io.grpc.stub.StreamObserver;


public class EvaluationServiceImpl extends EvaluationServiceGrpc.EvaluationServiceImplBase {
  public EvaluationServiceImpl() {
    super();
  }


  @Override
  public void evaluate(Bp.EvaluationRequest request, StreamObserver<Bp.EvaluationResponse> responseObserver) {
    String code = request.getIndividual().getCode().getCode();
    int gen = request.getIndividual().getGeneration();
    int id = request.getIndividual().getId();
    var evaluator = new RunnerEvaluator(code, gen, id);
    responseObserver.onNext(evaluator.call()); //take future
    responseObserver.onCompleted();
  }
}
