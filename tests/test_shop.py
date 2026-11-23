import csv
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages import LoginPage, InventoryPage, CartPage, CheckoutPage, CheckoutOverviewPage
import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "test_data.json"

with open(DATA_FILE) as file:
    test_data = json.load(file)
CSV_FILE = Path(__file__).resolve().parent.parent / "login_data.csv"

with open(CSV_FILE, newline="") as file:
    reader = csv.DictReader(file)
    login_cases = list(reader)
def test_valid_login_shows_six_products(driver):
    page = LoginPage(driver)
    page.open()
    page.login("standard_user", "secret_sauce")

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_name")))
    names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    assert len(names) == 6


@pytest.mark.parametrize(
    "username, password, expected_message",
    [
        (row["username"], row["password"], row["expected_error"])
        for row in login_cases
    ]
)
def test_invalid_login_shows_error(driver, username, password, expected_message):
    page = LoginPage(driver)
    page.open()
    page.login(username, password)
    assert expected_message in page.error_text()
def test_add_backpack_to_cart(driver):
    page = LoginPage(driver)
    page.open()
    page.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    inventory.add_backpack_to_cart()
    assert inventory.cart_count() == "1"
    cart = CartPage(driver)
    cart.open_cart()
    assert cart.product_name() == "Sauce Labs Backpack"
def test_remove_backpack_from_cart(driver):
    page = LoginPage(driver)
    page.open()
    page.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    inventory.add_backpack_to_cart()

    cart = CartPage(driver)
    cart.open_cart()
    cart.remove_backpack()

    assert cart.product_count() == 0

def test_checkout_information(driver):
    page = LoginPage(driver)
    page.open()
    page.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    inventory.add_backpack_to_cart()

    cart = CartPage(driver)
    cart.open_cart()
    cart.click_checkout()

    checkout = CheckoutPage(driver)
    checkout.enter_information(
    test_data["checkout_customer"]["first_name"],
    test_data["checkout_customer"]["last_name"],
    test_data["checkout_customer"]["postal_code"])
    checkout.click_continue()

    assert "checkout-step-two" in driver.current_url
def test_complete_checkout(driver):
    page = LoginPage(driver)
    page.open()
    page.login(
    test_data["valid_user"]["username"],
    test_data["valid_user"]["password"])
    inventory = InventoryPage(driver)
    inventory.add_backpack_to_cart()

    cart = CartPage(driver)
    cart.open_cart()
    cart.click_checkout()

    checkout = CheckoutPage(driver)
    checkout.enter_information(
    test_data["checkout_customer"]["first_name"],
    test_data["checkout_customer"]["last_name"],
    test_data["checkout_customer"]["postal_code"])
    checkout.click_continue()

    overview = CheckoutOverviewPage(driver)
    overview.finish_order()

    assert overview.confirmation_message() == "Thank you for your order!"
