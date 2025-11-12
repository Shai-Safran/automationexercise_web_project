import time
import threading
import sys
from colorama import Fore, Style, init
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from framework.logger import (
    log_info,
    log_success,
    log_error,
    log_warning,
    log_test_start,
    log_test_end
)

init(autoreset=True)


def timer_thread(start_time, stop_event, current_btn_text, print_lock):
    """תצוגת זמן ריצה חיה"""
    while not stop_event.is_set():
        elapsed = time.time() - start_time
        mins, secs = divmod(int(elapsed), 60)
        btn_display = current_btn_text[0] if current_btn_text[0] else "ממתין לכפתור..."
        with print_lock:
            sys.stdout.write(f"\r⏱️ זמן ריצה: {mins:02d}:{secs:02d} | בודק עכשיו: '{btn_display}'")
            sys.stdout.flush()
        time.sleep(1)
    print()  # מעבר שורה בסיום


def test_check_active_buttons_with_live_timer(headless=True):
    """בודק את כל הכפתורים/קישורים הפעילים באתר ומודד זמן ריצה בזמן אמת"""
    test_name = "בדיקת כפתורים פעילים באתר"
    log_test_start(test_name)

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # ← הרגיל במקום "--headless=new"
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)



    stats = {"success": 0, "warnings": 0, "errors": 0, "total": 0}
    outcome = "passed"

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    except Exception as e:
        log_error(f"שגיאה ביצירת ChromeDriver: {e}")
        log_test_end(test_name, "failed")
        return

    driver.maximize_window()
    url = "https://automationexercise.com/"
    start_time = time.time()
    log_info(f"🌐 טוען את האתר {url}")

    stop_event = threading.Event()
    current_btn_text = [""]
    print_lock = threading.Lock()

    t = threading.Thread(target=timer_thread, args=(start_time, stop_event, current_btn_text, print_lock))
    t.start()

    try:
        driver.get(url)

        try:
            all_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a | //button"))
            )
        except TimeoutException:
            log_warning("⚠️ לא נמצאו כפתורים או קישורים בדף")
            all_buttons = []

        log_info(f"נמצאו {len(all_buttons)} כפתורים/קישורים לבדיקה.")
        stats["total"] = len(all_buttons)

        for i, btn in enumerate(all_buttons, start=1):
            try:
                text = btn.text.strip() or btn.get_attribute("value") or "ללא טקסט"
                current_btn_text[0] = text

                if not btn.is_displayed() or not btn.is_enabled():
                    log_warning(f"⚠️ כפתור {i} '{text}' אינו לחיץ/גלוי.")
                    stats["warnings"] += 1
                    continue

                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                time.sleep(0.2)
                log_info(f"בודק כפתור {i}: '{text}'")

                old_url = driver.current_url
                old_source = driver.page_source
                href = btn.get_attribute("href")

                btn.click()
                log_info(f"🖱️ בוצעה לחיצה על '{text}'")

                try:
                    WebDriverWait(driver, 5).until(
                        lambda d: d.current_url != old_url or d.page_source != old_source
                    )
                except TimeoutException:
                    log_warning(f"⏳ לא זוהה שינוי בעמוד אחרי לחיצה על '{text}'")
                    stats["warnings"] += 1

                new_url = driver.current_url
                if href:
                    if href in new_url:
                        log_success(f"הניווט הצליח: {new_url}")
                        stats["success"] += 1
                    else:
                        log_warning(f"❌ הניווט שונה מהצפוי: {new_url}")
                        stats["warnings"] += 1
                else:
                    log_info("⏳ אין href – ייתכן שינוי תוכן פנימי בלבד")
                    stats["warnings"] += 1

            except StaleElementReferenceException:
                log_warning("⚠️ הכפתור השתנה במהלך הבדיקה (StaleElementReference)")
                stats["warnings"] += 1
                all_buttons = driver.find_elements(By.XPATH, "//a | //button")
            except Exception as e:
                log_error(f"שגיאה בכפתור {i}: '{text}' – {e}")
                stats["errors"] += 1
            finally:
                driver.get(url)
                try:
                    all_buttons = WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//a | //button"))
                    )
                except TimeoutException:
                    log_warning("⚠️ הדף נטען מחדש אך לא נמצאו כפתורים")
                    stats["warnings"] += 1
                    break

    except Exception as e:
        log_error(f"שגיאה כללית במהלך הבדיקה: {e}")
        stats["errors"] += 1
        outcome = "failed"

    finally:
        stop_event.set()
        t.join()
        duration = time.time() - start_time
        log_info(f"⏱️ משך הבדיקה הכולל: {duration:.2f} שניות")

        summary = (
            f"\n{'=' * 50}\n"
            f"📊 סיכום הבדיקה:\n"
            f"🔹 נבדקו: {stats['total']}\n"
            f"✅ הצלחות: {stats['success']}\n"
            f"⚠️ אזהרות: {stats['warnings']}\n"
            f"❌ שגיאות: {stats['errors']}\n"
            f"⏱️ משך כולל: {duration:.2f} שניות\n"
            f"{'=' * 50}\n"
        )

        log_info(summary)
        print(Fore.MAGENTA + summary + Style.RESET_ALL)

        if stats["errors"] > 0:
            outcome = "failed"

        log_test_end(test_name, outcome)
        driver.quit()


if __name__ == "__main__":
    test_check_active_buttons_with_live_timer(headless=True)
