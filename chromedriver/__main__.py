from concurrent.futures import ProcessPoolExecutor
from src.headless.driver import open
from src.grpc.server import serve

def main():
  pool = ProcessPoolExecutor()
  pool.submit(serve)

  # open("https://gateway.pinata.cloud/ipfs/QmXiSJPXJ8mf9LHijv6xFH1AtGef4h8v5VPEKZgjR4nzvM")

if __name__ == "__main__":
  main()
