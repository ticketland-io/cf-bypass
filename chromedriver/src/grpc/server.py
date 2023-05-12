import grpc
from concurrent import futures
from src.grpc.file_server_pb2_grpc import add_FileDownloaderServicer_to_server
from src.grpc.file_server_pb2_grpc import FileDownloaderServicer

def serve():
  print("Starting the gRPC server on port 50051")
  
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
  server.add_insecure_port('[::]:50051')
  server.start()
  
  print("gRPC server started on port 50051")
  
  server.wait_for_termination()
