import grpc
import bp_pb2_grpc as pb2_grpc
import bp_pb2


class ProtoClient(object):

    def __init__(self):
        self.host = '127.0.0.1'
        self.server_port = 8080

        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port), options=(('grpc.enable_http_proxy', 0), ('grpc.enable_https_proxy', 0),))

        self.stub = pb2_grpc.EvaluationServiceStub(self.channel)

    def get_url(self, individual):
        request = bp_pb2.EvaluationRequest(individual=individual)
        result = self.stub.Evaluate(request)
        # self.channel.close()
        return result
