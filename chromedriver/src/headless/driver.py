import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

def download(uri):
  chrome_options = Options()
  chrome_options.add_argument("--no-sandbox") # linux only
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9050")

  driver = uc.Chrome(options=chrome_options)
  
  driver.get(uri)
  data = driver.execute_script("let blob = new Blob({uri})")

  return data
