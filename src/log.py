from colorama import Fore, Style

class Log:
    @staticmethod
    def info(msg) -> None:
        print(f"{Style.DIM}[INFO]: {str(msg)}{Style.RESET_ALL}")

    @staticmethod
    def warning(msg) -> None:
        print(f"{Fore.YELLOW}[WARNING]: {str(msg)}{Fore.RESET}")

    @staticmethod
    def error(msg) -> None:
        print(f"{Fore.RED}[ERROR]: {str(msg)}{Fore.RESET}")

