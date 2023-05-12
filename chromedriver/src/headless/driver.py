import undetected_chromedriver as uc
import time
from selenium.webdriver.chrome.options import Options
import src.headless.js_scripts as js_scripts


def download(uri):
  chrome_options = Options()
  chrome_options.add_argument("--no-sandbox") # linux only
  chrome_options.add_argument("--headless")
  # chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9050")

  driver = uc.Chrome(options=chrome_options)
  driver.get(uri)

  start = time.perf_counter()
  data = driver.execute_async_script(js_scripts.convert_img_to_bytes(uri))
  end = time.perf_counter()
  print("time elapsed in ", end - start, sep='')
  
  return data
