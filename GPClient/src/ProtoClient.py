import grpc
import bp_pb2_grpc as pb2_grpc
import bp_pb2


class ProtoClient(object):

    def __init__(self):
        self.host = 'localhost'
        self.server_port = 8080

        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        self.stub = pb2_grpc.EvaluationServiceStub(self.channel)

    def get_url(self, individual):
        request = bp_pb2.EvaluationRequest(individual=individual)
        return self.stub.Evaluate(request)
