import optparse
import os
from colorama import Fore, init
from utils.get_from_file import get_from_file
from core.ILookup import ILookup
from utils.exit_banner import bb
import sys

init(autoreset=True)

def main():
    try:
        parser = optparse.OptionParser("usage: %prog -f <user agents file> -u <usernames file> -o <output file> -p <proxy_list>")
        parser.add_option("-u", "--usernames", dest="usernames_file", type="string", help="Specify the file path for usernames")
        parser.add_option("-a", "--agents", dest="user_agents", type="string", help="Specify the file path for user agents")
        parser.add_option("-o", "--output", dest="output_file", type="string", help="Specify the output file name (optional)")
        parser.add_option("-p", "--proxies", dest="proxy_list", type="string", help="Specify the proxy list file name (optional)")

        (options, _) = parser.parse_args()
        usernames_file = options.usernames_file
        user_agents_file = options.user_agents
        
        # optional arguments
        output_file = None
        proxy_list = None
        proxies = None

        #create folder if not exists
        if not os.path.exists("results"):
            os.makedirs("results")
        
        #load optional arguments
        if options.output_file:
            output_file = os.path.join("results", options.output_file)

        if options.proxy_list:
            proxy_list = options.proxy_list
        
        #check credentials
        if not usernames_file:
            print(Fore.RED + "[-] Please specify the file containing usernames with -u option.")
            exit(1)
        
        if not user_agents_file:
            print(Fore.RED + "[-] Please specify the user agents file with -a option.")
            exit(1)

        user_agents = get_from_file.load_user_agents(user_agents_file)
        usernames = get_from_file.get_users(usernames_file)
        if proxy_list:
            proxies = get_from_file.load_proxy_list(proxy_list)

        #second check
        if not user_agents:
            print(Fore.RED + "[-] User agents file is empty or cannot be read.")
            exit(1)

        if not usernames:
            print(Fore.RED + "[-] User agents file is empty or cannot be read.")
            exit(1)

        if output_file:
            print(Fore.GREEN + f"[+] Results will be saved to: {output_file}")
        if proxy_list and proxies:
            print(Fore.GREEN + f"[+] Proxy list loaded : {proxy_list}")
        
        # start instance
        lookup = ILookup(version="1.0.0", user_agents=user_agents,usernames=usernames,proxies=proxies)
        lookup.show_banner()

        if proxy_list and proxies:
            workingp = lookup.check_proxy()
            if workingp:
                print(Fore.GREEN + f"[+] Proxy list is working: {len(workingp)}")
            else:
                print(Fore.RED + f"[-] Proxy list is not working")

        lookup.process_usernames(output_file=output_file)
        
    except KeyboardInterrupt:
        bb()
        sys.exit(1)

if __name__ == "__main__":
    main()