from colorama import Fore

def banner(version):
    print(r"""
        .___                 __         .____                  __                 
        |   | ____   _______/  |______  |    |    ____   ____ |  | ____ ________  
        |   |/    \ /  ___/\   __\__  \ |    |   /  _ \ /  _ \|  |/ /  |  \____ \ 
        |   |   |  \\___ \  |  |  / __ \|    |__(  <_> |  <_> )    <|  |  /  |_> >
        |___|___|  /____  > |__| (____  /_______ \____/ \____/|__|_ \____/|   __/ 
                \/     \/            \/        \/                 \/     |__|    
            """ + f"\nInstaLookup by {Fore.RED}Grant{Fore.RED} {Fore.YELLOW}{version}{Fore.YELLOW}{Fore.RESET}")
