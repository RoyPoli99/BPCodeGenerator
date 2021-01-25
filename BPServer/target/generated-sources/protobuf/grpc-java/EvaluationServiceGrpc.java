import static io.grpc.MethodDescriptor.generateFullMethodName;
import static io.grpc.stub.ClientCalls.asyncBidiStreamingCall;
import static io.grpc.stub.ClientCalls.asyncClientStreamingCall;
import static io.grpc.stub.ClientCalls.asyncServerStreamingCall;
import static io.grpc.stub.ClientCalls.asyncUnaryCall;
import static io.grpc.stub.ClientCalls.blockingServerStreamingCall;
import static io.grpc.stub.ClientCalls.blockingUnaryCall;
import static io.grpc.stub.ClientCalls.futureUnaryCall;
import static io.grpc.stub.ServerCalls.asyncBidiStreamingCall;
import static io.grpc.stub.ServerCalls.asyncClientStreamingCall;
import static io.grpc.stub.ServerCalls.asyncServerStreamingCall;
import static io.grpc.stub.ServerCalls.asyncUnaryCall;
import static io.grpc.stub.ServerCalls.asyncUnimplementedStreamingCall;
import static io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall;

/**
 */
@javax.annotation.processing.Generated(
    value = "by gRPC proto compiler (version 1.24.0)",
    comments = "Source: bp.proto")
public final class EvaluationServiceGrpc {

  private EvaluationServiceGrpc() {}

  public static final String SERVICE_NAME = "EvaluationService";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<Bp.EvaluationRequest,
      Bp.EvaluationResponse> getEvaluateMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "Evaluate",
      requestType = Bp.EvaluationRequest.class,
      responseType = Bp.EvaluationResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<Bp.EvaluationRequest,
      Bp.EvaluationResponse> getEvaluateMethod() {
    io.grpc.MethodDescriptor<Bp.EvaluationRequest, Bp.EvaluationResponse> getEvaluateMethod;
    if ((getEvaluateMethod = EvaluationServiceGrpc.getEvaluateMethod) == null) {
      synchronized (EvaluationServiceGrpc.class) {
        if ((getEvaluateMethod = EvaluationServiceGrpc.getEvaluateMethod) == null) {
          EvaluationServiceGrpc.getEvaluateMethod = getEvaluateMethod =
              io.grpc.MethodDescriptor.<Bp.EvaluationRequest, Bp.EvaluationResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "Evaluate"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  Bp.EvaluationRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  Bp.EvaluationResponse.getDefaultInstance()))
              .setSchemaDescriptor(new EvaluationServiceMethodDescriptorSupplier("Evaluate"))
              .build();
        }
      }
    }
    return getEvaluateMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static EvaluationServiceStub newStub(io.grpc.Channel channel) {
    return new EvaluationServiceStub(channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static EvaluationServiceBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    return new EvaluationServiceBlockingStub(channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static EvaluationServiceFutureStub newFutureStub(
      io.grpc.Channel channel) {
    return new EvaluationServiceFutureStub(channel);
  }

  /**
   */
  public static abstract class EvaluationServiceImplBase implements io.grpc.BindableService {

    /**
     */
    public void evaluate(Bp.EvaluationRequest request,
        io.grpc.stub.StreamObserver<Bp.EvaluationResponse> responseObserver) {
      asyncUnimplementedUnaryCall(getEvaluateMethod(), responseObserver);
    }

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
          .addMethod(
            getEvaluateMethod(),
            asyncUnaryCall(
              new MethodHandlers<
                Bp.EvaluationRequest,
                Bp.EvaluationResponse>(
                  this, METHODID_EVALUATE)))
          .build();
    }
  }

  /**
   */
  public static final class EvaluationServiceStub extends io.grpc.stub.AbstractStub<EvaluationServiceStub> {
    private EvaluationServiceStub(io.grpc.Channel channel) {
      super(channel);
    }

    private EvaluationServiceStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected EvaluationServiceStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new EvaluationServiceStub(channel, callOptions);
    }

    /**
     */
    public void evaluate(Bp.EvaluationRequest request,
        io.grpc.stub.StreamObserver<Bp.EvaluationResponse> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(getEvaluateMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   */
  public static final class EvaluationServiceBlockingStub extends io.grpc.stub.AbstractStub<EvaluationServiceBlockingStub> {
    private EvaluationServiceBlockingStub(io.grpc.Channel channel) {
      super(channel);
    }

    private EvaluationServiceBlockingStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected EvaluationServiceBlockingStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new EvaluationServiceBlockingStub(channel, callOptions);
    }

    /**
     */
    public Bp.EvaluationResponse evaluate(Bp.EvaluationRequest request) {
      return blockingUnaryCall(
          getChannel(), getEvaluateMethod(), getCallOptions(), request);
    }
  }

  /**
   */
  public static final class EvaluationServiceFutureStub extends io.grpc.stub.AbstractStub<EvaluationServiceFutureStub> {
    private EvaluationServiceFutureStub(io.grpc.Channel channel) {
      super(channel);
    }

    private EvaluationServiceFutureStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected EvaluationServiceFutureStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new EvaluationServiceFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<Bp.EvaluationResponse> evaluate(
        Bp.EvaluationRequest request) {
      return futureUnaryCall(
          getChannel().newCall(getEvaluateMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_EVALUATE = 0;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final EvaluationServiceImplBase serviceImpl;
    private final int methodId;

    MethodHandlers(EvaluationServiceImplBase serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_EVALUATE:
          serviceImpl.evaluate((Bp.EvaluationRequest) request,
              (io.grpc.stub.StreamObserver<Bp.EvaluationResponse>) responseObserver);
          break;
        default:
          throw new AssertionError();
      }
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public io.grpc.stub.StreamObserver<Req> invoke(
        io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        default:
          throw new AssertionError();
      }
    }
  }

  private static abstract class EvaluationServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    EvaluationServiceBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return Bp.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("EvaluationService");
    }
  }

  private static final class EvaluationServiceFileDescriptorSupplier
      extends EvaluationServiceBaseDescriptorSupplier {
    EvaluationServiceFileDescriptorSupplier() {}
  }

  private static final class EvaluationServiceMethodDescriptorSupplier
      extends EvaluationServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final String methodName;

    EvaluationServiceMethodDescriptorSupplier(String methodName) {
      this.methodName = methodName;
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.MethodDescriptor getMethodDescriptor() {
      return getServiceDescriptor().findMethodByName(methodName);
    }
  }

  private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

  public static io.grpc.ServiceDescriptor getServiceDescriptor() {
    io.grpc.ServiceDescriptor result = serviceDescriptor;
    if (result == null) {
      synchronized (EvaluationServiceGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new EvaluationServiceFileDescriptorSupplier())
              .addMethod(getEvaluateMethod())
              .build();
        }
      }
    }
    return result;
  }
}
