import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)

    yield driver

    driver.quit()


@pytest.mark.parametrize("currency_index, currency_name", [
    ("2", "Доллары"),
    ("3", "Евро")
])
def test_foreign_currency_limit_validation(driver, currency_index, currency_name):
    wait = WebDriverWait(driver, 10)

    driver.get("http://localhost:8000/?balance=30000&reserved=20001")

    currency_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@role='button'][{currency_index}]")))
    currency_btn.click()

    card_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")))
    card_input.clear()
    card_input.send_keys("1234567812345678")

    amount_input = driver.find_element(By.XPATH, "//input[@placeholder='1000']")
    amount_input.clear()
    amount_input.send_keys("999")

    try:
        submit_button = driver.find_element(By.XPATH, "//span[@class='g-button__text']")

        if submit_button.is_displayed():
            pytest.fail(
                f"❌ БАГ ВОСПРОИЗВЕДЕН ({currency_name}): Кнопка «Перевести» появилась, хотя сумма перевода (50000) превышает баланс (30000)!")

    except (NoSuchElementException, TimeoutException):
        print(f"✅ Тест пройден для валюты {currency_name}: кнопка перевода недоступна.")
