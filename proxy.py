import requests
import time
import os
from os import path
import sys
from multiprocessing import Pool, Process, freeze_support, get_context, set_start_method

sys.tracebacklimit = 0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def padToCenter(l:list,w:int)->str:
    padding =  ' '*(w//2)
    parts = [ padding[0: (w-len(p))//2+1]+p for p in l]
    return '\n'.join(parts)

def welcome():
    width = os.get_terminal_size().columns
    os.system('cls' if os.name == 'nt' else 'clear')

    multi = """
        
        ██▓███   ██▀███   ▒█████  ▒██   ██▒▓██   ██▓                 
        ▓██░  ██▒▓██ ▒ ██▒▒██▒  ██▒▒▒ █ █ ▒░ ▒██  ██▒                 
        ▓██░ ██▓▒▓██ ░▄█ ▒▒██░  ██▒░░  █   ░  ▒██ ██░                 
        ▒██▄█▓▒ ▒▒██▀▀█▄  ▒██   ██░ ░ █ █ ▒   ░ ▐██▓░                 
        ▒██▒ ░  ░░██▓ ▒██▒░ ████▓▒░▒██▒ ▒██▒  ░ ██▒▓░                 
        ▒▓▒░ ░  ░░ ▒▓ ░▒▓░░ ▒░▒░▒░ ▒▒ ░ ░▓ ░   ██▒▒▒                  
        ░▒ ░       ░▒ ░ ▒░  ░ ▒ ▒░ ░░   ░▒ ░ ▓██ ░▒░                  
        ░░         ░░   ░ ░ ░ ░ ▒   ░    ░   ▒ ▒ ░░                   
                    ░         ░ ░   ░    ░   ░ ░                      
                                            ░ ░                      
  ██████  ▄████▄   ██▀███   ▄▄▄       ██▓███  ▓█████  ██▀███  
▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒▒████▄    ▓██░  ██▒▓█   ▀ ▓██ ▒ ██▒
░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▒██  ▀█▄  ▓██░ ██▓▒▒███   ▓██ ░▄█ ▒
  ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ░██▄▄▄▄██ ▒██▄█▓▒ ▒▒▓█  ▄ ▒██▀▀█▄  
▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒ ▓█   ▓██▒▒██▒ ░  ░░▒████▒░██▓ ▒██▒
▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░▒▓▒░ ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░  ▒   ▒▒ ░░▒ ░      ░ ░  ░  ░▒ ░ ▒░
░  ░  ░  ░          ░░   ░   ░   ▒   ░░          ░     ░░   ░ 
      ░  ░ ░         ░           ░  ░            ░  ░   ░     
         ░                                                    

    """

    print("-")
    print(padToCenter(multi.splitlines(), width))

    multi2 = """
[ ProxyScraper by cyclothymia ]
[ GitHub ++ https://github.com/cyclothymia/ProxyScraper ]
[ Make sure to star the project if you like it! ]

    """

    print("-")
    print(padToCenter(multi2.splitlines(), width))

def scrape():
    if path.exists("proxylist.txt"):
        os.remove("proxylist.txt")
    elif path.exists("proxytemp.txt"):
        os.remove("proxytemp.txt")

    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    payload = {}
    headers = {}

    print(bcolors.OKCYAN + "Scraping for proxies..." + bcolors.ENDC)

    response = requests.request("GET", url, headers=headers, data=payload)

    file = open("proxytemp.txt", "w")
    file.write(response.text)
    file.close

    print(bcolors.OKGREEN + "Scraping complete. Unchecked proxies are saved in proxytemp.txt" + bcolors.ENDC)
    print("""
    
    """)
    print(bcolors.OKCYAN + "Checking validity of proxies (this may take some time)..." + bcolors.ENDC)
    print(bcolors.FAIL + "Ignore the exception error that comes up. The program will continue to run as intended." + bcolors.ENDC)

def check(line):
    proxy = line.strip()
    try:
        requests.get("http://ipinfo.io/json", proxies={"http": "http://"+proxy}, timeout=5)
        file = open("proxylist.txt", "a")
        file.write(proxy + "\n")
        file.close
    except Exception as e:
        return

def main():
    set_start_method("spawn")
    proxies = open("proxytemp.txt")
    lines = proxies.readlines()
    s = time.time()
    p = Pool(processes=100)
    p.map(check, lines)
    t = time.time() - s
    print("""
    
    """)
    print(bcolors.OKGREEN + "Checking complete. Working proxy list saved to proxylist.txt" + bcolors.ENDC)
    print(bcolors.OKBLUE + f"Checking took {t} seconds." + bcolors.ENDC)
    print("")
    print(bcolors.OKCYAN + "You can delete proxytemp.txt since those are the unchecked proxies. Enjoy! :D" + bcolors.ENDC)

if __name__ == '__main__':
    freeze_support()
    welcome()
    scrape()
    main()
    quit()