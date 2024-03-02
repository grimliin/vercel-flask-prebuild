from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
import time
def main(stock):
  def expand_shadow_element(element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root
  options = Options()
  options.add_argument('log-level=3')
  options.add_argument('--headless')
  service = webdriver.EdgeService()

  driver = webdriver.Edge(options=options, service=service)
  driver.get('https://www.bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx/')
  print('waiting for cibserpmain')
  driver.implicitly_wait(30)
  print('done waiting')
  root1 = driver.find_element(By.CSS_SELECTOR, '.cib-serp-main')
  shadow_root1 = expand_shadow_element(root1)

  root2 = shadow_root1.find_element(By.ID,"cib-action-bar-main")
  shadow_root2 = expand_shadow_element(root2) 

  root3 = shadow_root2.find_element(By.CSS_SELECTOR,"cib-text-input[product='bing'][chat-type='consumer']")
  shadow_root3 = expand_shadow_element(root3)

  textArea = shadow_root3.find_element(By.ID, 'searchbox')
  #textArea.send_keys(Keys.TAB)
  textArea.send_keys(f'write me a sum of all event regarding {stock} in the last week in few sentences, as the forth point, add if you think the stock is looking bullish or bearish(dont nest your answers, just three bullet poitns, thanks)')
  textArea.send_keys(Keys.RETURN)
  time.sleep(20)
  driver.implicitly_wait(20)
  root2_1 = shadow_root1.find_element(By.ID, 'cib-conversation-main')
  shadow_root2_1 = expand_shadow_element(root2_1)

  root2_2 = shadow_root2_1.find_element(By.CSS_SELECTOR, "cib-chat-turn[serp-slot='none']")
  shadow_root2_2 = expand_shadow_element(root2_2)

  root2_3 = shadow_root2_2.find_element(By.CLASS_NAME, "response-message-group[class='response-message-group']")
  shadow_root2_3 = expand_shadow_element(root2_3)

  driver.implicitly_wait(5)
  root2_4 = shadow_root2_3.find_element(By.CSS_SELECTOR, "cib-message[type='text']")
  shadow_root2_4 = expand_shadow_element(root2_4)

  driver.implicitly_wait(5)
  message_box = shadow_root2_4.find_element(By.CSS_SELECTOR, "cib-shared[serp-slot='none']").find_element(By.CSS_SELECTOR,"div[class='content']")
  driver.implicitly_wait(5)
  texts = message_box.find_element(By.CSS_SELECTOR, "div[class='ac-container ac-adaptiveCard']").find_element(By.CSS_SELECTOR, "div[class='ac-textBlock']").find_elements(By.CSS_SELECTOR, "*")
  driver.implicitly_wait(5)
  result = []
  for i in texts:
      if i.tag_name == 'li':
          result.append(f'->{i.text[:-4]}<-')
  print('done executing')
  return stock, result
  