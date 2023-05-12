import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import src.headless.js_scripts as js_scripts

# Returns the page type: 'svg', 'img', 'pre' or None invalid page as well as the actual DOM element
def get_content_element(driver):
  body = driver.find_element(By.TAG_NAME, 'body')
  children = body.find_elements(By.CSS_SELECTOR, "*")
  
  child_elem = children[0]

  if len(children) > 0:
    return None, None
  elif child_elem.tag_name == "pre":
    return "pre", child_elem 
  elif child_elem.tag_name == "img":
    return "img", child_elem
  elif child_elem.tag_name == "svg":
    return "svg", child_elem
  else:
    return None, None
    
def download_gif(driver, uri):
  start = time.perf_counter()
  data = driver.execute_async_script(js_scripts.convert_img_to_bytes(uri))
  end = time.perf_counter()
  print("time elapsed in ", end - start, sep='')
  
  return data

def take_screenshot(driver):
  element = driver.find_elements_by_tag('img')
  return element.get_screenshot_as_png()

def download(uri):
  chrome_options = Options()
  chrome_options.add_argument("--no-sandbox") # linux only
  chrome_options.add_argument("--headless")
  # chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9050")

  driver = uc.Chrome(options=chrome_options)
  driver.get(uri)

  tag, elem = get_content_element(driver)

  if elem == None:
    return None
  elif tag == "pre":
    return bytes(elem.text())
  elif tag == "svg":
    return take_screenshot(driver)

  # If it's an image then check if it's gif so we use js script to get the data else just take a screenshot
  mime_type = driver.execute_async_script(js_scripts.get_mime_type(uri))
  print("Mime Type", mime_type)

  if mime_type == "image/gif":
    return download_gif(driver, uri)
  else:
    return take_screenshot(driver)
