/**
 * Insider Trading Scraper - Node.js Implementation
 * Integrates with your existing trading webhook stack
 *
 * Usage:
 *   node scrapers/index.js --ticker AAPL --interval 30
 *   node scrapers/index.js --watchlist tickers.txt
 */

import axios from 'axios';
import puppeteer from 'puppeteer';
import * as cron from 'node-cron';
import TelegramBot from 'node-telegram-bot-api';
import dotenv from 'dotenv';
import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const WEBHOOK_URL = process.env.WEBHOOK_URL || 'http://localhost:3000/webhook/insider-trading';
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID;

class InsiderTradingScraper {
    constructor(options = {}) {
        this.tickers = options.tickers || [];
        this.intervalMinutes = options.intervalMinutes || 30;
        this.webhookUrl = options.webhookUrl || WEBHOOK_URL;
        this.seenFilings = new Set();
        this.dataDir = path.join(__dirname, 'data');
        this.seenFile = path.join(this.dataDir, 'seen_filings.json');

        // Initialize Telegram bot if available
        this.bot = TELEGRAM_BOT_TOKEN ? new TelegramBot(TELEGRAM_BOT_TOKEN) : null;

        this.init();
    }

    async init() {
        // Create data directory
        await fs.mkdir(this.dataDir, { recursive: true });

        // Load seen filings
        await this.loadSeenFilings();

        console.log('Insider Trading Scraper initialized');
        console.log(`- Webhook: ${this.webhookUrl}`);
        console.log(`- Tickers: ${this.tickers.length > 0 ? this.tickers.join(', ') : 'All'}`);
        console.log(`- Interval: ${this.intervalMinutes} minutes`);
    }

    async loadSeenFilings() {
        try {
            const data = await fs.readFile(this.seenFile, 'utf8');
            this.seenFilings = new Set(JSON.parse(data));
            console.log(`Loaded ${this.seenFilings.size} seen filings`);
        } catch (error) {
            // File doesn't exist yet, start fresh
            this.seenFilings = new Set();
        }
    }

    async saveSeenFilings() {
        await fs.writeFile(
            this.seenFile,
            JSON.stringify([...this.seenFilings]),
            'utf8'
        );
    }

    isSeen(filingId) {
        return this.seenFilings.has(filingId);
    }

    markSeen(filingId) {
        this.seenFilings.add(filingId);
        // Save asynchronously in background
        this.saveSeenFilings().catch(console.error);
    }

    /**
     * Scrape SEC RSS feed for Form 4 filings
     */
    async scrapeSECRSS() {
        try {
            let url = 'https://www.sec.gov/cgi-bin/browse-edgar';

            if (this.tickers.length > 0) {
                // Scrape specific tickers
                const tickers = this.tickers.slice(0, 5); // Limit to 5
                url += `?action=getcompany&CIK=${tickers[0]}&type=4&count=20&owner=only&output=atom`;
            } else {
                // Scrape all recent filings
                url += '?action=getcurrent&type=4&count=100&owner=only&output=atom';
            }

            const response = await axios.get(url, {
                headers: {
                    'User-Agent': 'InsiderTradingScraper/1.0 (contact: your-email@example.com)',
                    'Accept': 'application/xml, application/rss+xml'
                },
                timeout: 30000
            });

            // Parse XML response
            const entries = this.parseRSSFeed(response.data);

            console.log(`Scraped ${entries.length} filings from SEC`);
            return entries;

        } catch (error) {
            console.error('Error scraping SEC RSS:', error.message);
            return [];
        }
    }

    /**
     * Parse SEC RSS feed
     */
    parseRSSFeed(xmlContent) {
        const entries = [];

        // Simple XML parsing (in production, use a proper XML parser)
        const entryRegex = /<entry>([\s\S]*?)<\/entry>/g;
        let match;

        while ((match = entryRegex.exec(xmlContent)) !== null) {
            const entryContent = match[1];

            const extractTag = (tagName) => {
                const tagMatch = new RegExp(`<${tagName}[^>]*>([\\s\\S]*?)<\\/${tagName}>`).exec(entryContent);
                return tagMatch ? tagMatch[1].trim() : '';
            };

            const extractAttr = (tagName, attrName) => {
                const tagMatch = new RegExp(`<${tagName}[^>]*${attrName}=["']([^"']*)["']`).exec(entryContent);
                return tagMatch ? tagMatch[1] : '';
            };

            const filingId = extractTag('accession-number') || extractAttr('link', 'href');

            entries.push({
                id: filingId,
                accession_number: extractTag('accession-number'),
                ticker: this.extractTicker(entryContent),
                company_name: extractTag('company-name') || extractTag('company-info'),
                cik: extractTag('cik'),
                filing_date: extractTag('filing-date'),
                filed_date: extractTag('date'),
                url: extractAttr('link', 'href'),
                summary: extractTag('summary')
            });
        }

        return entries;
    }

    /**
     * Extract ticker from content
     */
    extractTicker(content) {
        const tickerMatch = /Ticker:\s*([A-Z]{1,5})/i.exec(content);
        return tickerMatch ? tickerMatch[1].toUpperCase() : '';
    }

    /**
     * Scrape using Puppeteer for dynamic sites
     */
    async scrapeWithPuppeteer(url) {
        let browser;

        try {
            browser = await puppeteer.launch({
                headless: 'new',
                args: ['--no-sandbox', '--disable-setuid-sandbox']
            });

            const page = await browser.newPage();
            await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');

            await page.goto(url, {
                waitUntil: 'networkidle2',
                timeout: 30000
            });

            // Wait for content to load
            await page.waitForSelector('table', { timeout: 10000 });

            // Extract data
            const data = await page.evaluate(() => {
                const rows = document.querySelectorAll('table tbody tr');
                return Array.from(rows).slice(0, 20).map(row => {
                    const cols = row.querySelectorAll('td');
                    return {
                        ticker: cols[0]?.textContent?.trim() || '',
                        company: cols[1]?.textContent?.trim() || '',
                        insider: cols[2]?.textContent?.trim() || '',
                        transaction: cols[3]?.textContent?.trim() || '',
                        shares: cols[4]?.textContent?.trim() || '',
                        price: cols[5]?.textContent?.trim() || '',
                        date: cols[6]?.textContent?.trim() || ''
                    };
                });
            });

            await browser.close();
            return data;

        } catch (error) {
            console.error('Puppeteer scraping error:', error.message);
            if (browser) {
                await browser.close();
            }
            return [];
        }
    }

    /**
     * Send filing to webhook
     */
    async sendToWebhook(filing) {
        try {
            const payload = {
                type: 'insider_trading',
                ticker: filing.ticker,
                company: filing.company_name,
                filing_date: filing.filing_date,
                url: filing.url,
                timestamp: new Date().toISOString()
            };

            await axios.post(this.webhookUrl, payload, {
                headers: { 'Content-Type': 'application/json' },
                timeout: 10000
            });

            console.log(`✓ Sent webhook: ${filing.ticker} - ${filing.company_name}`);

        } catch (error) {
            console.error(`✗ Webhook failed: ${error.message}`);
        }
    }

    /**
     * Send Telegram notification
     */
    async sendTelegramAlert(filing) {
        if (!this.bot || !TELEGRAM_CHAT_ID) {
            return;
        }

        const emoji = filing.transaction?.toLowerCase()?.includes('buy') ? '🟢' : '🔴';

        const message = `
${emoji} <b>Insider Trading Alert</b>

🏢 <b>Company:</b> ${filing.company_name || 'N/A'}
📊 <b>Ticker:</b> <code>${filing.ticker || 'N/A'}</code>
📅 <b>Date:</b> ${filing.filing_date || 'N/A'}
${filing.url ? `🔗 <a href="${filing.url}">View Filing</a>` : ''}

🕐 ${new Date().toLocaleString()}
        `.trim();

        try {
            await this.bot.sendMessage(TELEGRAM_CHAT_ID, message, { parse_mode: 'HTML' });
            console.log(`✓ Telegram sent: ${filing.ticker}`);
        } catch (error) {
            console.error(`✗ Telegram failed: ${error.message}`);
        }
    }

    /**
     * Process filings
     */
    async processFilings(filings) {
        let newCount = 0;

        for (const filing of filings) {
            const filingId = filing.id || filing.accession_number;

            if (!filingId) {
                continue;
            }

            // Skip if already seen
            if (this.isSeen(filingId)) {
                continue;
            }

            // Mark as seen
            this.markSeen(filingId);

            // Send notifications
            await this.sendToWebhook(filing);
            await this.sendTelegramAlert(filing);

            newCount++;
        }

        return newCount;
    }

    /**
     * Run single check
     */
    async runOnce() {
        console.log('\n--- Running check ---');

        const filings = await this.scrapeSECRSS();
        const newCount = await this.processFilings(filings);

        console.log(`✓ Processed ${newCount} new filings\n`);
    }

    /**
     * Start continuous monitoring
     */
    start() {
        console.log('\n🚀 Starting continuous monitoring...\n');

        // Run immediately on start
        this.runOnce();

        // Schedule recurring runs
        const cronPattern = `*/${this.intervalMinutes} * * * *`;
        cron.schedule(cronPattern, () => {
            this.runOnce();
        });

        console.log(`✓ Monitoring started (checking every ${this.intervalMinutes} minutes)`);
        console.log('Press Ctrl+C to stop\n');
    }

    /**
     * Load tickers from file
     */
    static async loadWatchlist(filepath) {
        try {
            const content = await fs.readFile(filepath, 'utf8');
            return content
                .split('\n')
                .map(line => line.trim().toUpperCase())
                .filter(line => line && !line.startsWith('#'));
        } catch (error) {
            console.error(`Error loading watchlist: ${error.message}`);
            return [];
        }
    }
}

// CLI interface
async function main() {
    const args = process.argv.slice(2);

    // Parse arguments
    const options = {
        tickers: [],
        intervalMinutes: 30
    };

    let once = false;

    for (let i = 0; i < args.length; i++) {
        const arg = args[i];

        if (arg === '--ticker' && args[i + 1]) {
            options.tickers.push(args[++i].toUpperCase());
        } else if (arg === '--watchlist' && args[i + 1]) {
            const watchlistTickers = await InsiderTradingScraper.loadWatchlist(args[++i]);
            options.tickers.push(...watchlistTickers);
        } else if (arg === '--interval' && args[i + 1]) {
            options.intervalMinutes = parseInt(args[++i]);
        } else if (arg === '--once') {
            once = true;
        } else if (arg === '--help') {
            console.log(`
Usage: node scrapers/index.js [options]

Options:
  --ticker <SYMBOL>    Add ticker to monitor (can be used multiple times)
  --watchlist <FILE>   Load tickers from file (one per line)
  --interval <MINUTES> Check interval in minutes (default: 30)
  --once               Run once and exit
  --help               Show this help

Examples:
  node scrapers/index.js --ticker AAPL --ticker MSFT
  node scrapers/index.js --watchlist tickers.txt --interval 15
  node scrapers/index.js --once
            `);
            process.exit(0);
        }
    }

    // Create and start scraper
    const scraper = new InsiderTradingScraper(options);

    if (once) {
        await scraper.runOnce();
        process.exit(0);
    } else {
        scraper.start();
    }
}

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
    main().catch(console.error);
}

export default InsiderTradingScraper;
