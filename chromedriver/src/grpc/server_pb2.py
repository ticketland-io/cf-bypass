# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: server.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cserver.proto\x12\x10image_downloader\"\x16\n\x07Request\x12\x0b\n\x03uri\x18\x01 \x01(\t\",\n\x0c\x46ileResponse\x12\x0e\n\x06status\x18\x01 \x01(\r\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\x32[\n\x0e\x46ileDownloader\x12I\n\x0c\x44ownloadFile\x12\x19.image_downloader.Request\x1a\x1e.image_downloader.FileResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'server_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REQUEST._serialized_start=34
  _REQUEST._serialized_end=56
  _FILERESPONSE._serialized_start=58
  _FILERESPONSE._serialized_end=102
  _FILEDOWNLOADER._serialized_start=104
  _FILEDOWNLOADER._serialized_end=195
# @@protoc_insertion_point(module_scope)