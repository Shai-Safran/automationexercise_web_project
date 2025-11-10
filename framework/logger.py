import logging
import os
import time
from colorama import Fore, init

init(autoreset=True)

# --- ספריית הפרויקט הראשית ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- תיקיית הלוגים ---
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# --- קובץ לוג עם חותמת זמן ---
LOG_FILE = os.path.join(LOG_DIR, f"run_{time.strftime('%Y%m%d-%H%M%S')}.log")

# --- הגדרת logging ---
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding='utf-8'
)

# --- פונקציות עזר ללוגים צבעוניים ---
def log_info(msg):
    print(Fore.CYAN + msg)
    logging.info(msg)

def log_success(msg):
    print(Fore.GREEN + "✅ " + msg)
    logging.info(msg)

def log_warning(msg):
    print(Fore.YELLOW + "⚠️ " + msg)
    logging.warning(msg)

def log_error(msg):
    print(Fore.RED + "❌ " + msg)
    logging.error(msg)

def log_test_start(test_name):
    msg = f"--- STARTING TEST: {test_name} ---"
    print(Fore.BLUE + msg)
    logging.info(msg)

def log_test_end(test_name, outcome):
    status = "PASSED ✅" if outcome == "passed" else "FAILED ❌"
    msg = f"--- ENDING TEST: {test_name} - {status} ---"
    print(Fore.MAGENTA + msg)
    logging.info(msg)
