# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import logging
from src.grpc.file_server_pb2 import FileResponse

import src.grpc.file_server_pb2 as file__server__pb2
import src.headless.driver as chromedriver

class FileDownloaderStub(object):
		"""Missing associated documentation comment in .proto file."""

		def __init__(self, channel):
				"""Constructor.

				Args:
						channel: A grpc.Channel.
				"""
				self.DownloadFile = channel.unary_unary(
								'/file_server.FileDownloader/DownloadFile',
								request_serializer=file__server__pb2.Request.SerializeToString,
								response_deserializer=file__server__pb2.FileResponse.FromString,
								)


class FileDownloaderServicer(object):
	"""Missing associated documentation comment in .proto file."""
    
	def DownloadFile(self, request, context):
		"""Missing associated documentation comment in .proto file."""
		context.set_code(grpc.StatusCode.OK)
		print("Download file", request.uri)

		try:
			mime_type, data = chromedriver.download(request.uri)
			return FileResponse(mime_type=mime_type, data=data)
		except BaseException as exception:
			logging.exception("Error {exception}")
			
		return FileResponse

def add_FileDownloaderServicer_to_server(servicer, server):
		rpc_method_handlers = {
			'DownloadFile': grpc.unary_unary_rpc_method_handler(
				servicer.DownloadFile,
				request_deserializer=file__server__pb2.Request.FromString,
				response_serializer=file__server__pb2.FileResponse.SerializeToString,
			),
		}
		generic_handler = grpc.method_handlers_generic_handler('file_server.FileDownloader', rpc_method_handlers)
		server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FileDownloader(object):
		"""Missing associated documentation comment in .proto file."""

		@staticmethod
		def DownloadFile(request,
			target,
			options=(),
			channel_credentials=None,
			call_credentials=None,
			insecure=False,
			compression=None,
			wait_for_ready=None,
			timeout=None,
			metadata=None):
				return grpc.experimental.unary_unary(request, target, '/file_server.FileDownloader/DownloadFile',
						file__server__pb2.Request.SerializeToString,
						file__server__pb2.FileResponse.FromString,
						options, channel_credentials,
						insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
