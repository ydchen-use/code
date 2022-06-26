import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless'")
# chrome_options.add_argument('disable-infobars')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")

# driver = webdriver.Chrome("/Users/qianzhi/Downloads/chromedriver", options=chrome_options)
driver = webdriver.Remote("http://192.168.20.26:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME,
                          options=chrome_options)
driver.get("https://www.360bond.com")

time.sleep(1)
print(driver.page_source)


iframe = driver.find_element(by=By.CSS_SELECTOR, value="iframe")
print(iframe)
driver.switch_to.frame(iframe)

print(driver.page_source)
print(driver.current_url)

gif1 = driver.find_elements(by=By.CSS_SELECTOR, value="img")
num = 0
for item in gif1:
    item.screenshot("images/tmp/{}.png".format(num))
    num += 1
driver.save_screenshot("images/test.png")

driver.quit()
