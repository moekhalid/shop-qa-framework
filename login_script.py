from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

driver.get("https://www.saucedemo.com")

driver.find_element(By.ID, "user-name").send_keys("standard_user")
driver.find_element(By.ID, "password").send_keys("secret_sauce")
driver.find_element(By.ID, "login-button").click()

wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_name")))

names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")

print(f"Found {len(names)} products")
for name, price in zip(names, prices):
    print(name.text, price.text)

driver.quit()
   
