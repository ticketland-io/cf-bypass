import sys
from concurrent.futures import ProcessPoolExecutor
from src.grpc.server import serve

def main():
  args = sys.argv[1:]
  print(args)
  pool = ProcessPoolExecutor()
  pool.submit(serve(args[1]))

if __name__ == "__main__":
  main()
