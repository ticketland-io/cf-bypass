import undetected_chromedriver as uc

def main():
  print("hello world")
  
  driver = uc.Chrome()
  driver.get('https://gateway.pinata.cloud/ipfs/QmXiSJPXJ8mf9LHijv6xFH1AtGef4h8v5VPEKZgjR4nzvM')

if __name__ == "__main__":
  main() 
