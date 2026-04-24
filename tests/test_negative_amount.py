import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


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


def test_negative_amount_transfer_validation(driver):
    wait = WebDriverWait(driver, 10)

    driver.get("http://localhost:8000/?balance=30000&reserved=20001")

    rubles_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][1]")))
    rubles_btn.click()

    card_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")))
    card_input.clear()
    card_input.send_keys("1234567812345678")

    amount_input = driver.find_element(By.XPATH, "//input[@placeholder='1000']")
    amount_input.send_keys(Keys.CONTROL + "a")
    amount_input.send_keys(Keys.BACKSPACE)
    amount_input.send_keys("-58854")

    submit_button = driver.find_element(By.XPATH, "//span[@class='g-button__text']")
    submit_button.click()

    time.sleep(3)
    assert wait.until(EC.visibility_of_element_located((By.XPATH,
                                                        "//*[contains(@class, 'error')]"))), "БАГ ВОСПРОИЗВЕДЕН: Форма отправлена с суммой -500! Ошибка не появилась."
