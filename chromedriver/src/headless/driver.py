import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

def download(uri):
  chrome_options = Options()
  chrome_options.add_argument("--no-sandbox") # linux only
  chrome_options.add_argument("--headless")
  # chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9050")

  driver = uc.Chrome(options=chrome_options)
  
  driver.get(uri)

  js_script = """
  const img = document.querySelector('img');
  const imgCanvas = document.createElement('canvas');
  const imgContext = imgCanvas.getContext('2d');

  imgCanvas.width = img.width;
  imgCanvas.height = img.height;

  imgContext.drawImage(img, 0, 0, img.width, img.height);
  const imgData = imgContext.getImageData(0, 0, img.width, img.height);

  return imgData.data
  """.format(uri)

  data = driver.execute_script(js_script)

  return data
