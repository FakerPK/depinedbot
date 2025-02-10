# UPDATED: DePINed Network Automated Farming Bot For 100% Uptime
### Automate your connection to the DePINed API with this script. Manage multiple tokens and ensure 24/7 uptime. Join my Discord Server for invite codes.

![AGPL License](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)  
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)  
![Node.js](https://img.shields.io/badge/Node.js-16%2B-green)

## Features 🌟
* 🔄 Automatic proxy rotation
* 🔑 Multi-token support
* 🛡️ Cloudflare bypass
* 📊 SQLite database tracking
* 🚦 Connection state management
* 🌈 Colorful console interface

----
## Requirements 📋

#### 🏗️ Infrastructure

- **VPS Server**: AWS/GCP/DigitalOcean ($2-5/month)
- **ISP Proxies**: **MUST** use residential proxies (SOCKS5 format)
  - Recommended: [proxies.fo ISP Plan](https://app.proxies.fo/ref/f1353b58-10c4-98a5-d94d-6164e2efcfaf)
  ![Proxy Setup](https://github.com/user-attachments/assets/c81fc995-11f9-4448-9355-0065d4286cf2)

  ![Proxy Plan](https://github.com/user-attachments/assets/bbd22e0a-22c7-42cf-8608-361d7310e0ae)

<details>
<summary><strong>💻 Development Environment</strong></summary>

**Choose your language:**

<details>
<summary>Python 3.8+</summary>
For Linux:
  
```bash
# Install Python
sudo apt update
sudo apt install python3.11 python3-pip -y
```
For Windows:

```bash
# Download from Microsoft Store (easiest)
winget install Python.Python.3.11

# OR manual install
https://www.python.org/downloads/windows/
```
</details>

<details>
<summary>Node.js 16+</summary>
For Linux:
  
```bash
# Official PPA
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```
For Windows:

```bash
# Using winget
winget install OpenJS.NodeJS

# OR official installer
https://nodejs.org/en/download/
```
</details>
</details>
----


🔑 Token Extraction
-
1. Go to DePINed Dashboard
2. Press `CTRL + SHIFT + I`
3. In Console:
```javascript
localStorage.getItem('token')
```
![Token Extraction](https://github.com/user-attachments/assets/ea4dd3af-d0f6-40c3-bbb2-2243b3b79f30)


----
## Setup Guide 🛠️

### 1️⃣ Clone Repository
```bash
git clone https://github.com/FakerPK/depinedbot.git
cd depinedbot
```

### 2️⃣ Configuration Files

**config.json**
```json
{
    "tokens": [
        "your_first_token_here",
        "your_second_token_here"
    ]
}
```

**proxy.txt** (100+ recommended)
```json
socks5://username:pass@ip:port
socks5://username:pass@ip:port
```

### 3️⃣ Proxy Setup
1. Buy [ISP proxies](https://app.proxies.fo/ref/f1353b58-10c4-98a5-d94d-6164e2efcfaf)
2. Generate SOCKS5 proxies
3. Add them to the proxy file

### 4️⃣ Run Bot

<details>
<summary>Python Version Of The Script</summary>

```bash
pip -r requirements.txt
python3 main.py
```
</details>

<details>
<summary><strong>Javascript Version Script</strong></summary>

```java
npm install
node index.js
```
</details>

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
## Support 🆘  
Contact `FakerPK` on:  
<p align="center">
  <a href="https://t.me/+rurxli5cagplMjM8"><img width="60px" alt="Telegram" src="https://img.icons8.com/fluency/96/0088CC/telegram-app.png"/></a>
  <a href="https://discord.gg/mjzgatMCk8"><img width="60px" alt="Discord" src="https://img.icons8.com/fluency/96/FFA500/discord-logo.png"/></a> &#8287;
  <a href="https://medium.com/@FakerPK"><img width="60px" src="https://img.icons8.com/ios-filled/96/F0F0EC/medium-monogram.png" alt="Medium"></a>&#8287;
</p>

----
> **Warning**  
> ⚠️ Using datacenter proxies will result in **ZERO** earnings! Only use ISP proxies.
