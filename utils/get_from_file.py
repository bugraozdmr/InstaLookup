import sys
from functools import wraps
from colorama import Fore, Style, init
import random


init(autoreset=True)

def handle_file_errors(func):
    @wraps(func)
    def wrapper(file_path, *args, **kwargs):
        try:
            with open(file_path, 'r') as file:
                return func(file, *args, **kwargs)
        except FileNotFoundError:
            print(f"{Fore.RED}Error: The file '{file_path}' was not found.")
            sys.exit(1)
        except IOError:
            print(f"{Fore.RED}Error: An I/O error occurred while reading '{file_path}'.")
            sys.exit(1)
        except Exception as e:
            print(f"{Fore.RED}An unexpected error occurred: {e}")
            sys.exit(1)
    return wrapper

class get_from_file:
    @staticmethod
    @handle_file_errors
    def load_user_agents(file):
        return [line for line in file.read().splitlines() if line.strip()]


    @staticmethod
    @handle_file_errors
    def load_proxy_list(file):
        return [line for line in file.read().splitlines() if line.strip()]

    @staticmethod
    def get_random_user_agent(user_agents):
        return random.choice(user_agents)

    @staticmethod
    @handle_file_errors
    def get_users(file):
        return [line for line in file.read().splitlines() if line.strip()]