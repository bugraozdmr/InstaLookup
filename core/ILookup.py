from utils.banner import banner
from utils.get_from_file import get_from_file
from utils.write_file import write_file
from utils.dns_lookup import dnsL
import requests
from colorama import Fore
import json
import time
from functools import wraps


def time_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time  # Geçen süreyi hesapla
        print(f"\n{Fore.GREEN}Operation {func.__name__} executed in: {execution_time:.4f} seconds{Fore.GREEN}{Fore.RESET}")
        return result
    return wrapper

class ILookup:
    def __init__(self,version,user_agents=None,proxies=None,usernames=None):
        self.version = version
        self.user_agents = user_agents
        self.usernames = usernames
        self.proxies = proxies
        self.current_proxy = None
        self.current_index = 0

    def show_banner(self):
        banner(self.version)

    def get_instagram_profile(self,username, output_file=None):
        # avoid 429
        time.sleep(3)
        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    
        user_agent = get_from_file.get_random_user_agent(self.user_agents)
        headers = {
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Ig-App-Id': '936619743392459',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': f'https://www.instagram.com/{username}/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }

        if self.proxies:
            if self.proxies and len(self.proxies) != 0:
                self.current_proxy = self.proxies[0]
                print(f"Using proxy address : {Fore.GREEN}{self.current_proxy}{Fore.GREEN}{Fore.RESET}")
                
                proxy_parts = self.current_proxy.split(':')
                proxies = {
                    'https': f'http://{proxy_parts[2]}:{proxy_parts[3]}@{proxy_parts[0]}:{proxy_parts[1]}'
                }

                try:
                    response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
                except Exception as e:
                    self.proxies.pop(0)
                    self.current_index -= 1
                    print("This proxy is not working")
                    return None
            else:
                print("None of these given proxies are available")
                exit(1)
        else:
            if self.current_proxy:
                # if this is not none this means we had proxies but now we dont
                print("None of these given proxies are available")
                exit(1)
            else:
                response = requests.get(url, headers=headers, timeout=15)
    
        if response.status_code != 200:
            result = Fore.RED + f"[-] Failed to retrieve data for '{username}'. Status code: {response.status_code}\n"
            if output_file:
                write_file.write(output_file,f"[-] Failed to retrieve data for '{username}'. Status code: {response.status_code}\n")
            print(result)
            
            if not self.proxies:
                print("changing proxy\n")
                self.proxies.pop(0)
                self.current_index -= 1
            else:
                print(f"{Fore.RED}Something went wrong try sometime later{Fore.RED}{Fore.RESET}")
                exit(1)

            return None
        
        try:
            if not 'application/json' in response.headers.get('Content-Type', ''):
                if not self.proxies:
                    print(f"{Fore.RED}Response is not in JSON format Aborting{Fore.RED}{Fore.RESET}")
                    exit(1)
                else:
                    self.proxies.pop(0)
                    print(f"{Fore.RED}Response is not in JSON format Changing proxy{Fore.RED}{Fore.RESET}")
                    self.current_index -= 1
                    return None

            data = response.json()
            if data['status'] != 'ok':
                result = Fore.RED + f"[-] Failed to retrieve data for '{username}'. Status: {data['status']}\n"
                if output_file:
                    write_file.write(output_file,f"[-] Failed to retrieve data for '{username}'. Status: {data['status']}\n")
                print(result)
                return None
            
            user_data = data['data']['user']
            
            profile_info = {
                'username': user_data['username'],
                'full_name': user_data['full_name'],
                'bio': user_data['biography'],
                'profile_picture': user_data['profile_pic_url_hd'],
                'followers': user_data['edge_followed_by']['count'],
                'following': user_data['edge_follow']['count'],
                'posts': user_data['edge_owner_to_timeline_media']['count']
            }
            
            result = Fore.GREEN + "\n=== Profile Data ===\n"
            result_file = Fore.GREEN + "\n=== Profile Data ===\n"
            for key, value in profile_info.items():
                result += f"{Fore.YELLOW}{key.capitalize()}: {Fore.CYAN}{value}\n"
                result_file += f"{key.capitalize()}: {value}\n"
            
            print(result)
            if output_file:
                write_file.write(output_file,f"{result_file}\n")
                
        except (KeyError, json.JSONDecodeError) as e:
            result = Fore.RED + f"[-] Error parsing the JSON data for '{username}': {e}\n"
            if output_file:
                with open(output_file, 'a') as file:
                    file.write(f"[-] Error parsing the JSON data for '{username}': {e}\n")
            print(result)
    
    @time_execution
    def process_usernames(self, output_file=None):
        try:
            while self.current_index < len(self.usernames):
                print(Fore.MAGENTA + f"\nScanning profile for: {self.usernames[self.current_index]}")
                self.get_instagram_profile(self.usernames[self.current_index], output_file)

                self.current_index += 1

        except FileNotFoundError:
            print(Fore.RED + "[-] Usernames file not found.")
            exit(1)
        except Exception as e:
            print(Fore.RED + f"[-] An error occurred: {e}")
            exit(1)

    def check_proxy(self):
        dns = dnsL(proxies=self.proxies)
        return dns.process()