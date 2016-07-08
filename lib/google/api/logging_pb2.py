# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/api/logging.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/api/logging.proto',
  package='google.api',
  syntax='proto3',
  serialized_pb=_b('\n\x18google/api/logging.proto\x12\ngoogle.api\x1a\x1cgoogle/api/annotations.proto\"\xd7\x01\n\x07Logging\x12\x45\n\x15producer_destinations\x18\x01 \x03(\x0b\x32&.google.api.Logging.LoggingDestination\x12\x45\n\x15\x63onsumer_destinations\x18\x02 \x03(\x0b\x32&.google.api.Logging.LoggingDestination\x1a>\n\x12LoggingDestination\x12\x1a\n\x12monitored_resource\x18\x03 \x01(\t\x12\x0c\n\x04logs\x18\x01 \x03(\tB \n\x0e\x63om.google.apiB\x0cLoggingProtoP\x01\x62\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_LOGGING_LOGGINGDESTINATION = _descriptor.Descriptor(
  name='LoggingDestination',
  full_name='google.api.Logging.LoggingDestination',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='monitored_resource', full_name='google.api.Logging.LoggingDestination.monitored_resource', index=0,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='logs', full_name='google.api.Logging.LoggingDestination.logs', index=1,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=224,
  serialized_end=286,
)

_LOGGING = _descriptor.Descriptor(
  name='Logging',
  full_name='google.api.Logging',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='producer_destinations', full_name='google.api.Logging.producer_destinations', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='consumer_destinations', full_name='google.api.Logging.consumer_destinations', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_LOGGING_LOGGINGDESTINATION, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=71,
  serialized_end=286,
)

_LOGGING_LOGGINGDESTINATION.containing_type = _LOGGING
_LOGGING.fields_by_name['producer_destinations'].message_type = _LOGGING_LOGGINGDESTINATION
_LOGGING.fields_by_name['consumer_destinations'].message_type = _LOGGING_LOGGINGDESTINATION
DESCRIPTOR.message_types_by_name['Logging'] = _LOGGING

Logging = _reflection.GeneratedProtocolMessageType('Logging', (_message.Message,), dict(

  LoggingDestination = _reflection.GeneratedProtocolMessageType('LoggingDestination', (_message.Message,), dict(
    DESCRIPTOR = _LOGGING_LOGGINGDESTINATION,
    __module__ = 'google.api.logging_pb2'
    # @@protoc_insertion_point(class_scope:google.api.Logging.LoggingDestination)
    ))
  ,
  DESCRIPTOR = _LOGGING,
  __module__ = 'google.api.logging_pb2'
  # @@protoc_insertion_point(class_scope:google.api.Logging)
  ))
_sym_db.RegisterMessage(Logging)
_sym_db.RegisterMessage(Logging.LoggingDestination)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\016com.google.apiB\014LoggingProtoP\001'))
# @@protoc_insertion_point(module_scope)
