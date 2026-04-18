import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


def test_card_input_max_length(driver):
    wait = WebDriverWait(driver, 10)

    driver.get("http://localhost:8000/?balance=30000&reserved=20001")

    rubles_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][1]")))
    rubles_btn.click()

    card_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")))
    card_input.clear()

    test_card_number = "12345678123456789"
    card_input.send_keys(test_card_number)

    actual_value = card_input.get_attribute("value")

    actual_value_clean = actual_value.replace(" ", "")

    if len(actual_value_clean) == 17:
        pytest.fail(f"❌ БАГ ВОСПРОИЗВЕДЕН: Поле ввода приняло 17 цифр! Введенное значение: {actual_value}")

    assert len(actual_value_clean) == 16, f"Ожидалось 16 символов, но в поле: {len(actual_value_clean)}"
    print("✅ Тест пройден: поле ввода обрезало 17-й символ.")
