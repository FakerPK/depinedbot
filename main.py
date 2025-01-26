import json
import sqlite3
import requests
from requests.exceptions import RequestException
from threading import Timer
import time
from colorama import Fore, Style, init
import random

# Initialize colorama
init(autoreset=True)
polling_timer = None
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
    with open('proxy.txt', 'r') as file:
        return [line.strip() for line in file if line.strip()]

def remove_proxy_from_list(proxy):
    with open("proxy.txt", "r+") as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if line.strip() != proxy:
                file.write(line)
        file.truncate()

def poll_api():
    connection_state = get_value("connectionState")
    if not connection_state:
        print("Connection state is false, stopping polling", Fore.RED)
        return

    tokens = get_value("tokens") or []
    proxies = load_proxies()

    for token in tokens:
        if not proxies:  
            print("❌ No proxies available. Skipping token: {}".format(token), Fore.RED)
            continue

        for attempt in range(3):  # HOW MANY TIMES TO RETRY 
            proxy = random.choice(proxies) 
            try:
                start_time = time.time() 
                response = requests.post(
                    "https://api.depined.org/api/user/widget-connect",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {token}"
                    },
                    json={"connected": True},
                    proxies={"http": proxy, "https": proxy}  
                )
                elapsed_time = time.time() - start_time 
                if response.status_code == 200:
                    print(f"✅ API call successful for token: {token} using proxy: {proxy} (Time: {elapsed_time:.2f}s)")
                    break  
                else:
                    print(f"❌ API call failed with status: {response.status_code} using proxy: {proxy}", Fore.RED)
            except Exception as e:
                print(f"⚠️ Polling error for token {token} using proxy {proxy}: {str(e)}")
                remove_proxy_from_list(proxy)  

    if get_value("connectionState"):
        global polling_timer
        polling_timer = Timer(30, poll_api)  # PING INTERVAL
        polling_timer.start()


def start_polling():
    global polling_timer
    if polling_timer is None:
        poll_api()

def stop_polling():
    global polling_timer
    if polling_timer:
        polling_timer.cancel()
        polling_timer = None

def set_connection_state(is_connected):
    set_value("connectionState", is_connected)
    if is_connected:
        start_polling()
    else:
        stop_polling()

if __name__ == "__main__":
    print(f"""{Fore.YELLOW}
 ______    _             _____  _  __
|  ____|  | |           |  __ \| |/ /
| |__ __ _| | _____ _ __| |__) | ' / 
|  __/ _` | |/ / _ \ '__|  ___/|  <  
| | | (_| |   <  __/ |  | |    | . \ 
|_|  \__,_|_|\_\___|_|  |_|    |_|\_\ {Style.RESET_ALL}
    """)

    print(f"{Fore.MAGENTA}DePINed Bot! AUTOMATE AND DOMINATE{Style.RESET_ALL}")
    print(f"{Fore.RED}========================================{Style.RESET_ALL}")

    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            tokens = config.get("tokens", [])
            set_value("tokens", tokens)
    except FileNotFoundError:
        print("❌ Config file not found. Please create a config.json file with your tokens.")
        exit(1)
    except json.JSONDecodeError:
        print("❌ Invalid JSON in config file. Please check your config.json file.")
        exit(1)

    # CONNECTION STARTING LOGIC
    set_connection_state(True)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        set_connection_state(False)
        print("🛑 Connection logic simulation ended")
