import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from framework.logger_old import log_info

@pytest.fixture(scope="session")
def driver():
    log_info("🚀 מפעיל דפדפן Chrome...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    log_info("🚪 סוגר את הדפדפן...")
    driver.quit()
