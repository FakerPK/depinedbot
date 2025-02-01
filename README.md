# Ran Into Errors: DePINed Network Automated Farming Bot For 100% Uptime

### Automate your connection to the DePINed API with this Python-based script. This script manages multiple tokens and ensures 24/7 uptime for your connections. You can join my Discord Server for invite codes.

![AGPL License](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)

## Features
* Connects to the DePINed API using multiple tokens.
* Handles connection state management and error handling.
* Automatically retries connections and logs status with colorful output and emojis.
----
## Requirements
- **Python**: Install Python from [python.org](https://www.python.org/downloads/) (available for Windows and macOS) or on Ubuntu Server using the following command:
  ```bash
  sudo apt install python3
- **VPS Server**: You can obtain a VPS server through AWS Free Tier, Google Cloud Free Tier, or any other online provider for approximately $2-5 per month.
- **Proxy Server**: It is essential to purchase only ISP residential proxies to earn points. Using data center or free proxies will result in zero earnings. Recommended proxy providers include:
- **Proxies.fo**: Visit [https://app.proxies.fo](https://app.proxies.fo/ref/f1353b58-10c4-98a5-d94d-6164e2efcfaf) Purchase only the 1GB plan, which is sufficient for 1-6 months and allows for unlimited accounts or proxies.
- **DePINed Token:** A valid token from the DePINed API, Here's how to extract it:
  - Go to the DePINed Dashboard, Press CTRL + SHIFT + i and enter:
    ```bash
    localStorage.getItem('token')
    ```
    ![image](https://github.com/user-attachments/assets/ea4dd3af-d0f6-40c3-bbb2-2243b3b79f30)
  - Copy the Token and save it.
- Basic knowledge of running Python scripts.
----
## If You Want To Buy Proxies From My Recommended Provider Follow These Steps
1. Go to [https://app.proxies.fo](https://app.proxies.fo/ref/f1353b58-10c4-98a5-d94d-6164e2efcfaf) and Sign Up.
2. Go to the ISP section, DONOT BUY THE RESIDENTIAL PLAN OR ELSE THIS WON'T WORK:
![image](https://github.com/user-attachments/assets/c81fc995-11f9-4448-9355-0065d4286cf2)
3. Buy one of these plans, remember DONOT BUY THE RESIDENTIAL PLAN ONLY BUY THE ISP PLAN:
![image](https://github.com/user-attachments/assets/bbd22e0a-22c7-42cf-8608-361d7310e0ae)
4. Now you're going to generate SOCKS5 proxies, and add them to the proxy.txt file.
----
## Steps to Run the Code

Before running the script, ensure you have Python installed on your machine. Then, install the necessary Python packages using:

#### 1. Clone the repo:
```bash
git clone https://github.com/FakerPK/depinedbot.git
```
#### 2. Change Directory
```bash
cd depinedbot
```
#### 3. Install required packages
```python
pip install -r requirements.txt
```
#### 4. Create a config.json file:
In the project directory, create a config.json file with the following structure:

```json
{
    "tokens": [
        "your_first_token_here",
        "your_second_token_here"
    ]
}
```
#### 5. Add proxies to `proxy.txt` file
The proxies should be in the following format:
```json 
socks5://username:pass@ip:port
```
Add atleast 100 proxies so that malfuntioning proxies can be removed.
#### 6. Run the script
To execute the script, use the following command:
```bash
python3 main.py
```
----
##  **💸Donations**
If you would like to support me or the development of this projects, you can make a donation using the following addresses:
- **Solana :**
```bash
9SqcZjiUAz9SYBBLwuA9uJG4UzwqC5HNWV2cvXPk3Kro
```
- **EVM :**
```bash
0x2d550c8A47c60A43F8F4908C5d462184A40922Ef
```
- **BTC :**
```bash
bc1qhx7waktcttam9q9nt0ftdguguwg5lzq5hnasmm
```
----
## FOR ANY KIND OF HELP CONTACT : ` FakerPK` on Discord  https://discord.com/users/1087110214559473766
----
# SOCIALS -

- **Telegram** - [https://t.me/FakerPK](https://t.me/FakerPK)
- **Discord** - [https://discord.gg/pGJSPtp9zz](https://discord.gg/Z58YmYwr))
