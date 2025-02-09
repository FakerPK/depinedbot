# Copyright (C) 2025 FakerPK
# Licensed under the AGPL-3.0: https://www.gnu.org/licenses/agpl-3.0.html
# This software is provided "as-is" without any warranties.
import json
import sqlite3
from curl_cffi import requests
from fake_useragent import FakeUserAgent
from threading import Timer
import time
from colorama import Fore, Style, init
import random

init(autoreset=True)
polling_timers = []

def open_database():
    conn = sqlite3.connect('extension.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings
    (key TEXT PRIMARY KEY, value TEXT)
    ''')
    conn.commit()
    return conn

def set_value(key, value):
    conn = open_database()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                   (key, json.dumps(value)))
    conn.commit()
    conn.close()

def get_value(key):
    conn = open_database()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    result = cursor.fetchone()
    conn.close()
    return json.loads(result[0]) if result else None

def load_proxies():
    try:
        with open('proxy.txt', 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []

def remove_proxy_from_list(proxy):
    with open("proxy.txt", "r+") as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if line.strip() != proxy:
                file.write(line)
        file.truncate()

class CloudflareBypassSession(requests.Session):
    def __init__(self):
        super().__init__()
        self.impersonate = "chrome120"
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": FakeUserAgent().random,
            "X-Requested-With": "XMLHttpRequest"
        }

    def rotate_headers(self):
        self.headers["User-Agent"] = FakeUserAgent().random

def poll_api():
    connection_state = get_value("connectionState")
    if not connection_state:
        print(f"{Fore.RED}🛑 Connection state is false, stopping polling")
        return

    tokens = get_value("tokens") or []
    proxies = load_proxies()

    for token in tokens:
        session = CloudflareBypassSession()
        success = False
        
        for attempt in range(3):
            proxy = random.choice(proxies) if proxies else None
            try:
                session.rotate_headers()
                response = session.post(
                    "https://api.depined.org/api/user/widget-connect",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {token}",
                        "Origin": "https://app.depined.org",
                        "Referer": "https://app.depined.org/"
                    },
                    json={"connected": True},
                    proxy=proxy,
                    timeout=30
                )
                
                if response.status_code == 200:
                    print(f"{Fore.GREEN}✅ {Style.BRIGHT}Success for {token[:8]}...{Style.RESET_ALL}"
                          f"{Fore.LIGHTBLUE_EX} using {proxy}{Style.RESET_ALL}")
                    success = True
                    break
                else:
                    print(f"{Fore.YELLOW}⚠️ {Style.BRIGHT}Attempt {attempt+1} failed (Code {response.status_code})")
                    if response.status_code == 403:
                        remove_proxy_from_list(proxy)
                        proxies = load_proxies()
            except Exception as e:
                print(f"{Fore.RED}❌ {Style.BRIGHT}Connection error: {str(e)}")
                if proxy:
                    remove_proxy_from_list(proxy)
                    proxies = load_proxies()

        if not success:
            print(f"{Fore.RED}🔴 {Style.BRIGHT}All attempts failed for {token[:8]}...")

    if get_value("connectionState"):
        t = Timer(30, poll_api)
        polling_timers.append(t)
        t.start()

def start_polling():
    stop_polling()
    poll_api()

def stop_polling():
    for t in polling_timers:
        t.cancel()
    polling_timers.clear()

def cleanup():
    stop_polling()

if __name__ == "__main__":
    print(f"""{Fore.YELLOW + Style.BRIGHT}
    ███████╗ █████╗ ██╗  ██╗███████╗██████╗  ██████╗ ██╗  ██╗ 
    ██╔════╝██╔══██╗██║ ██╔╝██╔════╝██╔══██╗ ██╔══██╗██║ ██╔╝ 
    █████╗  ███████║█████╔╝ █████╗  ██████╔╝ ██████╔╝█████╔╝  
    ██╔══╝  ██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗ ██╔═══╝ ██╔═██╗  
    ██║     ██║  ██║██║  ██╗███████╗██║  ██║ ██║     ██║  ██╗     
    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═╝     ╚═╝  ╚═╝     
{Style.RESET_ALL}
    """)

    print(f"{Fore.LIGHTBLUE_EX + Style.BRIGHT}🚀 DePINed Bot! AUTOMATE AND DOMINATE{Style.RESET_ALL}")
    print(f"{Fore.RED}═══════════════════════════════════════════════════{Style.RESET_ALL}")


    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            tokens = config.get("tokens", [])
            set_value("tokens", tokens)
            print(f"{Fore.GREEN}✅ {Style.BRIGHT}Loaded {len(tokens)} tokens{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ {Style.BRIGHT}Config error: {str(e)}{Style.RESET_ALL}")
        exit(1)

    set_value("connectionState", True)
    start_polling()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}🛑 {Style.BRIGHT}Shutting down...{Style.RESET_ALL}")
        cleanup()
        set_value("connectionState", False)
        print(f"{Fore.GREEN}✅ {Style.BRIGHT}Cleanup complete{Style.RESET_ALL}")
# Copyright (C) 2025 FakerPK
# Licensed under the AGPL-3.0: https://www.gnu.org/licenses/agpl-3.0.html
# This software is provided "as-is" without any warranties.
# Adding this to make the language percentage equal for better searh results
# Adding this to make the language percentage equal for better searh results
# Adding this to make the language percentage equal for better searh results
# Adding this to make the language percentage equal for
