import requests
import os
from colorama import Fore

# TODO all proxy types support http(s)/sock4/sock5...

class dnsL:
    def __init__(self,proxies):
        self.proxies = proxies
        self.working_proxies = []

    def check_proxy(self,proxy):
        # example proxy : 206.41.271.74:6634:auctz32134:ki314i6egpgrx

        # this works better
        url = 'https://api.ipify.org'


        proxy_parts = proxy.split(':')
        if len(proxy_parts) < 4:
            return False
        
        proxy_ip = proxy_parts[0]
        proxy_port = proxy_parts[1]
        proxy_user = proxy_parts[2]
        proxy_pass = proxy_parts[3]

        # instagram only accepts https proxies
        proxies = {
            'https': f'http://{proxy_user}:{proxy_pass}@{proxy_ip}:{proxy_port}',
        }

        try:
            response = requests.get(url, proxies=proxies, timeout=5)
            if response.status_code == 200:
                self.working_proxies.append(proxy)
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            #print(f"Proxy {proxy} failed: {e}")
            return False

    def process(self):
        count = len(self.proxies)
        print(f"\n{Fore.CYAN}Checking proxies ...{Fore.CYAN}{Fore.YELLOW}\n{count} entrys{Fore.YELLOW}{Fore.RESET}")

        for index, proxy in enumerate(self.proxies, start=1):
            print(f"{index}/{count}")

            self.check_proxy(proxy)
            print("\033[F\033[K", end='')

        return self.working_proxies