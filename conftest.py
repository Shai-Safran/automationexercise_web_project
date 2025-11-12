import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # <-- הוספת ייבוא Options
from webdriver_manager.chrome import ChromeDriverManager
from framework.logger import log_info, log_warning, log_error, log_success, log_test_start, log_test_end


@pytest.fixture(scope="session")
def driver():
    log_info("🚀 מפעיל דפדפן Chrome...")

    # ----------------------------------------------------
    # הגדרת אופציות ה-Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # ← הרגיל במקום "--headless=new"
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--remote-debugging-port=9222")

    # אתחול הדרייבר עם האופציות
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options  # <-- העברת האופציות
    )
    # ----------------------------------------------------

    # מכיוון שהוספת --window-size, אין צורך ב-maximize_window(), אבל נשאיר למען הבטיחות
    driver.maximize_window()

    # טוען את עמוד הבית של האתר הנבדק
    driver.get("https://automationexercise.com/")

    yield driver
    log_info("🚪 סוגר את הדפדפן...")
    driver.quit()