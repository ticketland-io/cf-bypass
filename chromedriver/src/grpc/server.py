import grpc
from concurrent import futures
from src.grpc.server_pb2_grpc import add_FileDownloaderServicer_to_server
from src.grpc.server_pb2_grpc import FileDownloaderServicer

def serve():
  print("Starting the gRPC server on port 50051")

  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  add_FileDownloaderServicer_to_server(FileDownloaderServicer(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  
  print("gRPC server started on port 50051")
  
  server.wait_for_termination()
