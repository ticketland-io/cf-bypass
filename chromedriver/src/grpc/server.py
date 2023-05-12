import grpc
from concurrent import futures
from src.grpc.file_server_pb2_grpc import add_FileDownloaderServicer_to_server
from src.grpc.file_server_pb2_grpc import FileDownloaderServicer

def serve(port="[::]:50051"):
  print("Starting the gRPC server on port {}".format(port))
  
  kb = 1024
  mb = 1024*kb
  max_message_size = 50 * mb
  
  server = grpc.server(
    futures.ThreadPoolExecutor(max_workers=10),
    options=[
      ('grpc.max_send_message_length', max_message_size),
      ('grpc.max_receive_message_length', max_message_size),
    ]
  )
  add_FileDownloaderServicer_to_server(FileDownloaderServicer(), server)
  server.add_insecure_port(port)
  server.start()
  
  print("gRPC server started on port {}".format(port))
  
  server.wait_for_termination()
