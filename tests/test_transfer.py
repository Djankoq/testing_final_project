import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
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


def test_empty_amount_transfer_fails(driver):
    url = "http://localhost:8000/?balance=30000&reserved=20001"
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    rubles = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='button'][1]")))
    rubles.click()

    card_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")))
    card_input.clear()
    card_input.send_keys("1234567812345678")

    amount_input = driver.find_element(By.XPATH, "//input[@placeholder='1000']")
    amount_input.send_keys(Keys.CONTROL + "a")
    amount_input.send_keys(Keys.BACKSPACE)

    submit_button = driver.find_element(By.XPATH, "//span[@class='g-button__text']")
    submit_button.click()

    try:
        error_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".error-message")))
        assert error_message.is_displayed()

    except Exception:
        pytest.fail("БАГ: Сообщение об ошибке не отобразилось! Перевод с пустой суммой пропущен.")