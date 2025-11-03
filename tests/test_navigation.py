import logging
import time
from colorama import Fore, Style, init
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

init(autoreset=True)

# הגדרת לוגים
logging.basicConfig(
    filename=f"logs/test_{time.strftime('%Y%m%d_%H%M%S')}.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_info(msg):
    print(Fore.CYAN + msg)
    logging.info(msg)

def log_warning(msg):
    print(Fore.YELLOW + "⚠️ " + msg)
    logging.warning(msg)

def log_success(msg):
    print(Fore.GREEN + "✅ " + msg)
    logging.info(msg)

def log_error(msg):
    print(Fore.RED + "❌ " + msg)
    logging.error(msg)


def test_navigate_to_test_cases():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    url = "https://automationexercise.com/"
    start_time = time.time()
    log_info(f"🌐 Loading {url}")

    driver.get(url)

    try:
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

        # בדיקה של מקרי הבדיקה
        test_cases = driver.find_elements(By.CLASS_NAME, "panel-group")
        log_info(f"נמצאו {len(test_cases)} מקרי בדיקה.")

        if len(test_cases) == 0:
            log_warning("לא נמצאו מקרי בדיקה בעמוד!")

    except Exception as e:
        log_error(f"שגיאה במהלך הבדיקה: {e}")

    finally:
        duration = time.time() - start_time
        log_info(f"⏱️ משך הבדיקה: {duration:.2f} שניות")
        driver.quit()
