from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "https://www.saucedemo.com"
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME).send_keys(username)
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def error_text(self):
        error = self.wait.until(EC.visibility_of_element_located(self.ERROR))
        return error.text
class InventoryPage:
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ADD_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def product_count(self):
        self.wait.until(
            EC.presence_of_all_elements_located(self.PRODUCT_NAMES)
        )
        products = self.driver.find_elements(*self.PRODUCT_NAMES)
        return len(products)
    
    def add_backpack_to_cart(self):
        self.wait.until(
            EC.element_to_be_clickable(self.ADD_BACKPACK)
        ).click()

    def cart_count(self):
        badge = self.wait.until(
            EC.visibility_of_element_located(self.CART_BADGE)
        )
        return badge.text
class CartPage:
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    REMOVE_BACKPACK = (By.ID, "remove-sauce-labs-backpack")
    CART_ITEM = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_cart(self):
        self.driver.find_element(*self.CART_LINK).click()

    def product_name(self):
        item = self.wait.until(
            EC.visibility_of_element_located(self.CART_ITEM)
        )
        return item.text

    
    
    def remove_backpack(self):
        wait = WebDriverWait(
            self.driver,
            15,
            ignored_exceptions=(StaleElementReferenceException,)
        )
        wait.until(
            EC.element_to_be_clickable(self.REMOVE_BACKPACK)
        ).click()

     
    def product_count(self):
        items = self.driver.find_elements(*self.CART_ITEM)
        return len(items)
    def click_checkout(self):
        button = self.wait.until(
            EC.element_to_be_clickable(self.CHECKOUT_BUTTON)
        )
        button.click()
class CheckoutPage:
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")

    def __init__(self, driver):
        self.driver = driver

    def enter_information(self, first, last, zip_code):
        wait = WebDriverWait(self.driver, 10)

        first_name = wait.until(
            EC.visibility_of_element_located(self.FIRST_NAME)
        )

        first_name.send_keys(first)
        self.driver.find_element(*self.LAST_NAME).send_keys(last)
        self.driver.find_element(*self.POSTAL_CODE).send_keys(zip_code)
    def click_continue(self):
        self.driver.find_element(*self.CONTINUE_BUTTON).click()

class CheckoutOverviewPage:
    FINISH_BUTTON = (By.ID, "finish")
    COMPLETE_MESSAGE = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def finish_order(self):
        button = self.wait.until(
            EC.element_to_be_clickable(self.FINISH_BUTTON)
        )
        button.click()

    def confirmation_message(self):
        message = self.wait.until(
            EC.visibility_of_element_located(self.COMPLETE_MESSAGE)
        )
        return message.text
