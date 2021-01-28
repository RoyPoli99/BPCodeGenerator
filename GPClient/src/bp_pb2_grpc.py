# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import bp_pb2 as bp__pb2


class EvaluationServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Evaluate = channel.unary_unary(
                '/EvaluationService/Evaluate',
                request_serializer=bp__pb2.EvaluationRequest.SerializeToString,
                response_deserializer=bp__pb2.EvaluationResponse.FromString,
                )


class EvaluationServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Evaluate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_EvaluationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Evaluate': grpc.unary_unary_rpc_method_handler(
                    servicer.Evaluate,
                    request_deserializer=bp__pb2.EvaluationRequest.FromString,
                    response_serializer=bp__pb2.EvaluationResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'EvaluationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class EvaluationService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Evaluate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/EvaluationService/Evaluate',
            bp__pb2.EvaluationRequest.SerializeToString,
            bp__pb2.EvaluationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)