import logging
import time
from colorama import Fore, Style, init
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from framework.logger import log_info, log_success, log_error, log_warning, log_test_start, log_test_end

init(autoreset=True)


def test_navigate_to_test_cases(headless=True):
    """בדיקה של ניווט לכפתור Test Cases והפעלת כל מקרי הבדיקה"""
    test_name = "בדיקת ניווט לכפתור Test Cases"
    log_test_start(test_name)

    # --- הגדרת Chrome Options ל-headless ---
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")  # שימוש ב-headless רגיל
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--remote-debugging-port=9222")

    outcome = "passed"

    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        # רק אם לא headless
        if not headless:
            driver.maximize_window()

        url = "https://automationexercise.com/"
        start_time = time.time()
        log_info(f"🌐 Loading {url}")
        driver.get(url)

        # --- ניווט לכפתור Test Cases ---
        button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@href='/test_cases']"))
        )
        log_success("כפתור 'Test Cases' נמצא וגלוי לעין")

        if not button.is_enabled():
            log_warning("הכפתור מופיע אך אינו פעיל כרגע.")
        else:
            button.click()
            log_info("🖱️ בוצעה לחיצה על 'Test Cases'")

        WebDriverWait(driver, 10).until(EC.url_contains("/test_cases"))
        log_success("הניווט לעמוד Test Cases הצליח")

        # --- בדיקה של מקרי הבדיקה ---
        test_cases = driver.find_elements(By.CLASS_NAME, "panel-group")
        log_info(f"נמצאו {len(test_cases)} מקרי בדיקה.")
        if len(test_cases) == 0:
            log_warning("לא נמצאו מקרי בדיקה בעמוד!")

        accordion_headers = driver.find_elements(By.XPATH, "//*[@id='form']//h4/a")

        for i, header in enumerate(accordion_headers, start=1):
            try:
                header_text = header.text.strip()
                driver.execute_script("arguments[0].scrollIntoView(true);", header)
                time.sleep(0.2)

                header.click()
                log_info(f"נפתח Test Case {i}: {header_text}")

                content = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, f"//*[@id='form']//div[@id='collapse{i}']")
                    )
                )

                if content.is_displayed():
                    log_success(f"✅ התוכן מוצג עבור Test Case {i}")
                    if header_text.lower() in content.text.lower():
                        log_success(f"✅ הטקסט בתוכן תואם את הכותרת: '{header_text}'")
                    else:
                        log_warning(f"❌ הטקסט בתוכן לא תואם את הכותרת: '{header_text}'")
                else:
                    log_warning(f"❌ התוכן לא מוצג עבור Test Case {i}")

            except Exception as e:
                log_error(f"❌ שגיאה בבדיקת Test Case {i}: {e}")

    except Exception as e:
        log_error(f"שגיאה במהלך הבדיקה: {e}")
        outcome = "failed"

    finally:
        duration = time.time() - start_time
        log_info(f"⏱️ משך הבדיקה: {duration:.2f} שניות")
        driver.quit()
        log_test_end(test_name, outcome)


if __name__ == "__main__":
    # ריצה ב-headless
    test_navigate_to_test_cases(headless=True)
