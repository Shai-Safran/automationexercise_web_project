import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from framework.logger_old import log_info, log_success, log_error
import pytest

@pytest.mark.regression
def test_testcases_page(driver):
    """בודקת ניווט לעמוד ה-Test Cases וספירת מקרי הבדיקה"""
    driver.get("https://automationexercise.com/")
    log_info("🔎 מחפש את הכפתור 'Test Cases'...")
    start = time.time()

    try:
        test_case_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@href='/test_cases']"))
        )
        test_case_button.click()

        WebDriverWait(driver, 10).until(EC.url_contains("/test_cases"))
        test_cases = driver.find_elements(By.CLASS_NAME, "panel-group")

        duration = time.time() - start
        log_success(f"✅ נמצאו {len(test_cases)} מקרי בדיקה תוך {duration:.2f} שניות")

        assert len(test_cases) > 0, "לא נמצאו מקרי בדיקה"
    except Exception as e:
        log_error(f"❌ שגיאה בעת ניווט לעמוד ה-Test Cases: {e}")
        raise
