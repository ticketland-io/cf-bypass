import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import src.headless.js_scripts as js_scripts

class Driver:
  _instance = None

  def __new__(cls, *args, **kwargs):
    # If no instance of class already exits
    if cls._instance is None:
      cls._instance = object.__new__(cls)
      cls._instance._initialized = False

    return cls._instance

  def __init__(self):
    if self._initialized:
      return
          
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox") # linux only
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    start = time.perf_counter()
    self.driver = uc.Chrome(options=chrome_options)
    end = time.perf_counter()
    print("create Chrome elapsed in ", end - start, sep='')

    self._initialized = True

  def download(self, uri):
    start = time.perf_counter()
    self.driver.get(uri)
    end = time.perf_counter()
    print("Open tab elapsed in ", end - start, sep='')

    tag, elem = self.get_content_element()

    print("Tag Name", tag)

    if elem == None:
      return None, None
    elif tag == "pre":
      return "application/json", bytes(elem.text, 'utf-8')
    elif tag == "svg":
      return "image/svg+xml", self.take_screenshot()

    # If it's an image then check if it's gif so we use js script to get the data else just take a screenshot
    mime_type = self.driver.execute_async_script(js_scripts.get_mime_type(uri))
    print("Mime Type", mime_type)

    if mime_type == "image/gif":
      return mime_type, self.download_gif(uri)
    else:
      return mime_type, self.take_screenshot()

  # Returns the page type: 'svg', 'img', 'pre' or None invalid page as well as the actual DOM element
  def get_content_element(self):
    body = self.driver.find_element(By.TAG_NAME, 'body')
    children = body.find_elements(By.CSS_SELECTOR, "*")
    child_elem = children[0]  

    if len(children) == 0:
      return None, None
    elif child_elem.tag_name == "pre":
      return "pre", child_elem 
    elif child_elem.tag_name == "img":
      return "img", child_elem
    elif child_elem.tag_name == "svg":
      return "svg", child_elem
    else:
      return None, None
      
  def download_gif(self, uri):
    start = time.perf_counter()
    data = self.driver.execute_async_script(js_scripts.convert_img_to_bytes(uri))
    end = time.perf_counter()
    print("time elapsed in ", end - start, sep='')
    
    return data

  def take_screenshot(self):
    element = self.driver.find_element(By.TAG_NAME, 'img')
    return element.screenshot_as_png
