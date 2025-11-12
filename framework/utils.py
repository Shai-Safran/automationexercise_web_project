from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from typing import Tuple, Union
from .logger import log_info, log_warning, log_error, log_success

DEFAULT_TIMEOUT = 10

# Safe click with scrolling
def safe_click(driver, element):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(element))
        element.click()
        log_success("לחיצה בוצעה בהצלחה")
    except Exception as e:
        log_error(f"שגיאה ב-safe_click: {e}")
        raise

# Wait for element to be clickable
def wait_for_clickable(driver, by, value, timeout=20):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        return element
    except Exception as e:
        log_error(f"לא ניתן למצוא אלמנט לחיץ: {value} ({e})")
        raise

# Hover over element
def hover_over_element(driver, element):
    try:
        ActionChains(driver).move_to_element(element).perform()
        log_info("Hover over element executed")
    except Exception as e:
        log_error(f"שגיאה ב-hover_over_element: {e}")
        raise

# Remove overlays / popups (example: modals, ads)
def remove_all_overlays(driver):
    try:
        # דוגמה: סוגר מודאלים לפי class
        overlays = driver.find_elements(By.CLASS_NAME, "overlay")
        for overlay in overlays:
            try:
                overlay.click()
            except:
                driver.execute_script("arguments[0].remove();", overlay)
        log_info("כל הפרסומות/overlay מוסרו בהצלחה")
    except Exception as e:
        log_warning(f"אזהרה בהסרת overlays: {e}")


def wait_for_clickable(
        driver: WebDriver,
        by_type: str,
        locator: str,
        timeout: int = DEFAULT_TIMEOUT
) -> Union[WebElement, None]:
    """
    ממתין עד שאלמנט ה-Web ימצא ויהיה לחיץ, ומחזיר אותו.

    :param driver: אובייקט ה-WebDriver.
    :param by_type: שיטת האיתור (לדוגמה: By.XPATH, By.ID, וכו').
    :param locator: המחרוזת המשמשת לאיתור האלמנט.
    :param timeout: זמן ההמתנה המקסימלי בשניות.
    :return: אובייקט WebElement אם נמצא, אחרת None (תוך זריקת שגיאה בתוך ה-logger).
    """
    try:
        # יצירת אובייקט WebDriverWait
        wait = WebDriverWait(driver, timeout)

        # המתנה עד שהאלמנט יהיה נוכח ב-DOM וניתן ללחיצה
        element = wait.until(
            EC.element_to_be_clickable((by_type, locator))
        )
        return element

    except TimeoutException:
        # טיפול בכשל בזמן
        error_message = f"❌ ERROR: פסק זמן (Timeout) - לא ניתן למצוא אלמנט לחיץ: {locator}"
        log_error(error_message)
        # זורק את השגיאה הלאה כדי שהבדיקה תיכשל כצפוי
        raise TimeoutException(error_message)

    except NoSuchElementException:
        # טיפול בכשל במציאת האלמנט
        error_message = f"❌ ERROR: האלמנט לא נמצא (NoSuchElement) ב-DOM: {locator}"
        log_error(error_message)
        raise NoSuchElementException(error_message)

    except WebDriverException as e:
        # טיפול בשגיאות דרייבר כלליות (כמו InvalidSessionIdException אם ה-timeout נכשל)
        error_message = f"❌ ERROR: שגיאת WebDriver כללית בעת המתנה לאלמנט {locator}: {e}"
        log_error(error_message)
        raise WebDriverException(error_message)
