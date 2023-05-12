import undetected_chromedriver as uc

def open(uri):
  driver = uc.Chrome()
  driver.get(uri)
