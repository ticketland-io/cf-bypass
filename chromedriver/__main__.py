from concurrent.futures import ProcessPoolExecutor
from src.grpc.server import serve

def main():
  pool = ProcessPoolExecutor()
  pool.submit(serve)

if __name__ == "__main__":
  main()
