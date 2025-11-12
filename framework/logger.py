from colorama import init, Fore, Style
init(autoreset=True)

def log_info(message):
    print(f"{Fore.CYAN}ℹ️  INFO: {message}{Style.RESET_ALL}")

def log_success(message):
    print(f"{Fore.GREEN}✅ SUCCESS: {message}{Style.RESET_ALL}")

def log_warning(message):
    print(f"{Fore.YELLOW}⚠️  WARNING: {message}{Style.RESET_ALL}")

def log_error(message):
    print(f"{Fore.RED}❌ ERROR: {message}{Style.RESET_ALL}")

def log_test_start(test_name):
    print(f"{Fore.MAGENTA}🚀 STARTING TEST: {test_name}{Style.RESET_ALL}")

def log_test_end(test_name, status):
    status_icon = "✅" if status.lower() == "passed" else "❌"
    color = Fore.GREEN if status.lower() == "passed" else Fore.RED
    print(f"{color}{status_icon} ENDING TEST: {test_name} - {status.upper()}{Style.RESET_ALL}")
