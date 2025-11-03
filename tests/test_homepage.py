import time
from framework.logger import log_info, log_success, log_error
import pytest

@pytest.mark.smoke
def test_homepage_loads(driver):
    """בודקת שהעמוד הראשי נטען בהצלחה"""
    url = "https://automationexercise.com/"
    start = time.time()
    log_info(f"🌐 טוען את האתר: {url}")
    driver.get(url)
    time.sleep(2)
    try:
        assert "Automation Exercise" in driver.title
        duration = time.time() - start
        log_success(f"✅ העמוד הראשי נטען בהצלחה תוך {duration:.2f} שניות")
    except AssertionError:
        log_error("❌ כשל בטעינת העמוד הראשי")
        raise
