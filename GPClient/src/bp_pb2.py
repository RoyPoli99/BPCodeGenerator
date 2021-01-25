# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bp.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='bp.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x08\x62p.proto\"\x15\n\x05\x62prog\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\"B\n\nIndividual\x12\x12\n\ngeneration\x18\x01 \x01(\x05\x12\n\n\x02id\x18\x02 \x01(\x05\x12\x14\n\x04\x63ode\x18\x03 \x01(\x0b\x32\x06.bprog\"4\n\x11\x45valuationRequest\x12\x1f\n\nindividual\x18\x01 \x01(\x0b\x32\x0b.Individual\"1\n\x12\x45valuationResponse\x12\x0c\n\x04wins\x18\x01 \x01(\x05\x12\r\n\x05\x64raws\x18\x02 \x01(\x05\x32H\n\x11\x45valuationService\x12\x33\n\x08\x45valuate\x12\x12.EvaluationRequest\x1a\x13.EvaluationResponseb\x06proto3'
)




_BPROG = _descriptor.Descriptor(
  name='bprog',
  full_name='bprog',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='bprog.code', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=12,
  serialized_end=33,
)


_INDIVIDUAL = _descriptor.Descriptor(
  name='Individual',
  full_name='Individual',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='generation', full_name='Individual.generation', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id', full_name='Individual.id', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='code', full_name='Individual.code', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=35,
  serialized_end=101,
)


_EVALUATIONREQUEST = _descriptor.Descriptor(
  name='EvaluationRequest',
  full_name='EvaluationRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='individual', full_name='EvaluationRequest.individual', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=103,
  serialized_end=155,
)


_EVALUATIONRESPONSE = _descriptor.Descriptor(
  name='EvaluationResponse',
  full_name='EvaluationResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='wins', full_name='EvaluationResponse.wins', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='draws', full_name='EvaluationResponse.draws', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=157,
  serialized_end=206,
)

_INDIVIDUAL.fields_by_name['code'].message_type = _BPROG
_EVALUATIONREQUEST.fields_by_name['individual'].message_type = _INDIVIDUAL
DESCRIPTOR.message_types_by_name['bprog'] = _BPROG
DESCRIPTOR.message_types_by_name['Individual'] = _INDIVIDUAL
DESCRIPTOR.message_types_by_name['EvaluationRequest'] = _EVALUATIONREQUEST
DESCRIPTOR.message_types_by_name['EvaluationResponse'] = _EVALUATIONRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

bprog = _reflection.GeneratedProtocolMessageType('bprog', (_message.Message,), {
  'DESCRIPTOR' : _BPROG,
  '__module__' : 'bp_pb2'
  # @@protoc_insertion_point(class_scope:bprog)
  })
_sym_db.RegisterMessage(bprog)

Individual = _reflection.GeneratedProtocolMessageType('Individual', (_message.Message,), {
  'DESCRIPTOR' : _INDIVIDUAL,
  '__module__' : 'bp_pb2'
  # @@protoc_insertion_point(class_scope:Individual)
  })
_sym_db.RegisterMessage(Individual)

EvaluationRequest = _reflection.GeneratedProtocolMessageType('EvaluationRequest', (_message.Message,), {
  'DESCRIPTOR' : _EVALUATIONREQUEST,
  '__module__' : 'bp_pb2'
  # @@protoc_insertion_point(class_scope:EvaluationRequest)
  })
_sym_db.RegisterMessage(EvaluationRequest)

EvaluationResponse = _reflection.GeneratedProtocolMessageType('EvaluationResponse', (_message.Message,), {
  'DESCRIPTOR' : _EVALUATIONRESPONSE,
  '__module__' : 'bp_pb2'
  # @@protoc_insertion_point(class_scope:EvaluationResponse)
  })
_sym_db.RegisterMessage(EvaluationResponse)



_EVALUATIONSERVICE = _descriptor.ServiceDescriptor(
  name='EvaluationService',
  full_name='EvaluationService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=208,
  serialized_end=280,
  methods=[
  _descriptor.MethodDescriptor(
    name='Evaluate',
    full_name='EvaluationService.Evaluate',
    index=0,
    containing_service=None,
    input_type=_EVALUATIONREQUEST,
    output_type=_EVALUATIONRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_EVALUATIONSERVICE)

DESCRIPTOR.services_by_name['EvaluationService'] = _EVALUATIONSERVICE

# @@protoc_insertion_point(module_scope)
