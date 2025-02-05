const sqlite3 = require('sqlite3').verbose();
const { open } = require('sqlite');
const fs = require('fs');
const chalk = require('chalk');
const { HttpsProxyAgent } = require('https-proxy-agent');
const axios = require('axios');
const { getRandomUserAgent } = require('random-useragent');

// Initialize database
let db;
async function openDatabase() {
    return open({
        filename: 'extension.db',
        driver: sqlite3.Database
    });
}

async function initializeDatabase() {
    db = await openDatabase();
    await db.exec(`
        CREATE TABLE IF NOT EXISTS settings 
        (key TEXT PRIMARY KEY, value TEXT)
    `);
}

async function setValue(key, value) {
    await db.run(
        "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
        [key, JSON.stringify(value)]
    );
}

async function getValue(key) {
    const result = await db.get(
        "SELECT value FROM settings WHERE key = ?",
        [key]
    );
    return result ? JSON.parse(result.value) : null;
}

// Proxy handling
function loadProxies() {
    try {
        return fs.readFileSync('proxy.txt', 'utf8')
            .split('\n')
            .filter(line => line.trim());
    } catch (e) {
        return [];
    }
}

function removeProxyFromList(proxy) {
    const proxies = loadProxies();
    const newProxies = proxies.filter(p => p !== proxy);
    fs.writeFileSync('proxy.txt', newProxies.join('\n'));
}

// Session class
class CloudflareBypassSession {
    constructor() {
        this.headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "X-Requested-With": "XMLHttpRequest"
        };
        this.rotateHeaders();
    }

    rotateHeaders() {
        this.headers['User-Agent'] = getRandomUserAgent();
    }

    async request(config) {
        this.rotateHeaders();
        return axios({
            ...config,
            headers: {
                ...this.headers,
                ...config.headers
            },
            httpsAgent: config.proxy ? new HttpsProxyAgent(config.proxy) : undefined,
            timeout: 30000
        });
    }
}

// Polling logic
let pollingTimeout;
let active = false;

async function pollApi() {
    if (!active) return;

    const connectionState = await getValue("connectionState");
    if (!connectionState) {
        console.log(chalk.red.bold("🛑 Connection state is false, stopping polling"));
        active = false;
        return;
    }

    const tokens = await getValue("tokens") || [];
    let proxies = loadProxies();

    for (const token of tokens) {
        const session = new CloudflareBypassSession();
        let success = false;

        for (let attempt = 0; attempt < 3; attempt++) {
            const proxy = proxies.length > 0 
                ? proxies[Math.floor(Math.random() * proxies.length)]
                : null;

            try {
                const response = await session.request({
                    method: 'post',
                    url: 'https://api.depined.org/api/user/widget-connect',
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`,
                        "Origin": "https://app.depined.org",
                        "Referer": "https://app.depined.org/"
                    },
                    data: { connected: true },
                    proxy
                });

                if (response.status === 200) {
                    console.log(
                        chalk.green.bold(`✅ Success for ${token.substring(0,8)}...`) + ' ' +
                        chalk.blue(`using ${proxy}`)
                    );
                    success = true;
                    break;
                } else {
                    console.log(chalk.yellow.bold(
                        `⚠️ Attempt ${attempt+1} failed (Code ${response.status})`
                    ));
                    if (response.status === 403 && proxy) {
                        removeProxyFromList(proxy);
                        proxies = loadProxies();
                    }
                }
            } catch (error) {
                console.log(chalk.red.bold(`❌ Connection error: ${error.message}`));
                if (proxy) {
                    removeProxyFromList(proxy);
                    proxies = loadProxies();
                }
            }
        }

        if (!success) {
            console.log(chalk.red.bold(`🔴 All attempts failed for ${token.substring(0,8)}...`));
        }
    }

    if (active) {
        pollingTimeout = setTimeout(pollApi, 30000);
    }
}

function startPolling() {
    stopPolling();
    active = true;
    pollApi();
}

function stopPolling() {
    clearTimeout(pollingTimeout);
    active = false;
}

async function cleanup() {
    stopPolling();
    await setValue("connectionState", false);
    await db.close();
}

// Main execution
(async () => {
    await initializeDatabase();
    
    console.log(chalk.yellow.bold(`
    ███████╗ █████╗ ██╗  ██╗███████╗██████╗  ██████╗ ██╗  ██╗ 
    ██╔════╝██╔══██╗██║ ██╔╝██╔════╝██╔══██╗ ██╔══██╗██║ ██╔╝ 
    █████╗  ███████║█████╔╝ █████╗  ██████╔╝ ██████╔╝█████╔╝  
    ██╔══╝  ██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗ ██╔═══╝ ██╔═██╗  
    ██║     ██║  ██║██║  ██╗███████╗██║  ██║ ██║     ██║  ██╗     
    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═╝     ╚═╝  ╚═╝     
    `));
    console.log(chalk.blue.bold("🚀 DePINed Bot! AUTOMATE AND DOMINATE"));
    console.log(chalk.red("═══════════════════════════════════════════════════"));

    try {
        const config = JSON.parse(fs.readFileSync('config.json', 'utf8'));
        await setValue("tokens", config.tokens);
        console.log(chalk.green.bold(`✅ Loaded ${config.tokens.length} tokens`));
    } catch (e) {
        console.log(chalk.red.bold(`❌ Config error: ${e.message}`));
        process.exit(1);
    }

    await setValue("connectionState", true);
    startPolling();

    process.on('SIGINT', async () => {
        console.log(chalk.yellow.bold("\n🛑 Shutting down..."));
        await cleanup();
        console.log(chalk.green.bold("✅ Cleanup complete"));
        process.exit();
    });
})();
