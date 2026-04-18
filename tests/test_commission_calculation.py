import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


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


def test_commission_calculation_under_100_rubles(driver):
    wait = WebDriverWait(driver, 10)

    driver.get("http://localhost:8000/?balance=30000&reserved=20001")

    rubles_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][1]")))
    rubles_btn.click()

    card_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")))
    card_input.clear()
    card_input.send_keys("1234567812345678")

    test_amount = 50
    amount_input = driver.find_element(By.XPATH, "//input[@placeholder='1000']")
    amount_input.clear()
    amount_input.send_keys(str(test_amount))

    time.sleep(0.5)

    commission_element = driver.find_element(By.XPATH, "//span[@id='comission']")

    actual_commission_text = commission_element.text

    try:
        actual_commission = float(actual_commission_text)
    except ValueError:
        pytest.fail(f"Не удалось распарсить значение комиссии: '{commission_element.text}'")

    expected_commission = test_amount * 0.10

    if actual_commission == 0 and expected_commission > 0:
        pytest.fail(
            f"❌ БАГ ВОСПРОИЗВЕДЕН: Комиссия для {test_amount} руб. равна 0! Ожидалось: {expected_commission} руб. (Возможно проблема с округлением на фронтенде).")

    assert actual_commission == expected_commission, f"Неверный расчет комиссии. Ожидалось: {expected_commission}, Фактически: {actual_commission}"

    print(f"✅ Тест пройден: комиссия рассчитана верно ({actual_commission} руб.)")