/**
 * Insider Trading Service
 * Integrates SEC data with your trading webhook stack
 */

import axios from 'axios';
import { logger } from '../utils/logger.js';

const SEC_BASE_URL = 'https://www.sec.gov';
const COMPANY_TICKERS_URL = 'https://www.sec.gov/files/company_tickers.json';

// Cache for ticker to CIK mappings
const tickerCache = new Map();

/**
 * Get CIK for a ticker symbol
 */
async function getCIK(ticker) {
  ticker = ticker.toUpperCase();

  // Check cache first
  if (tickerCache.has(ticker)) {
    return tickerCache.get(ticker);
  }

  // Load all mappings if not cached
  if (tickerCache.size === 0) {
    await loadTickerMappings();
  }

  return tickerCache.get(ticker) || null;
}

/**
 * Load ticker to CIK mappings from SEC
 */
async function loadTickerMappings() {
  try {
    logger.info('Loading SEC ticker mappings...');
    const response = await axios.get(COMPANY_TICKERS_URL, {
      headers: {
        'User-Agent': 'Trading Webhook Stack (trading@example.com)',
        'Accept': 'application/json'
      }
    });

    const data = response.data;
    for (const item of Object.values(data)) {
      const ticker = item.ticker.toUpperCase();
      const cik = String(item.cik_str).padStart(10, '0');
      tickerCache.set(ticker, cik);
    }

    logger.info(`Loaded ${tickerCache.size} ticker mappings`);
  } catch (error) {
    logger.error('Failed to load ticker mappings:', error.message);
  }
}

/**
 * Get recent Form 4 filings for a ticker
 */
async function getRecentForm4Filings(ticker, daysBack = 30) {
  const cik = await getCIK(ticker);

  if (!cik) {
    throw new Error(`Ticker ${ticker} not found`);
  }

  const url = `${SEC_BASE_URL}/Archives/edgar/data/${cik.replace(/^0+/, '')}/CIK${cik}.json`;

  try {
    const response = await axios.get(url, {
      headers: {
        'User-Agent': 'Trading Webhook Stack (trading@example.com)',
        'Accept': 'application/json'
      }
    });

    const data = response.data;
    const filings = data.filings.recent;

    // Filter for Form 4
    const form4Filings = [];
    for (let i = 0; i < filings.form.length; i++) {
      if (filings.form[i] === '4') {
        const filingDate = new Date(filings.filingDate[i]);
        const cutoffDate = new Date();
        cutoffDate.setDate(cutoffDate.getDate() - daysBack);

        if (filingDate >= cutoffDate) {
          form4Filings.push({
            accession_number: filings.accessionNumber[i],
            filing_date: filings.filingDate[i],
            form: filings.form[i],
            cik: cik,
            ticker: ticker
          });
        }
      }
    }

    logger.info(`Found ${form4Filings.length} Form 4 filings for ${ticker}`);
    return form4Filings;

  } catch (error) {
    logger.error(`Failed to fetch filings for ${ticker}:`, error.message);
    throw error;
  }
}

/**
 * Monitor multiple tickers and return formatted alerts
 */
async function monitorTickers(tickers) {
  const results = [];

  for (const ticker of tickers) {
    try {
      const filings = await getRecentForm4Filings(ticker, 7); // Last 7 days

      if (filings.length > 0) {
        results.push({
          ticker,
          filing_count: filings.length,
          latest_filing: filings[0].filing_date,
          filings: filings.slice(0, 3) // Include top 3
        });
      }
    } catch (error) {
      logger.error(`Error monitoring ${ticker}:`, error.message);
    }
  }

  return results;
}

/**
 * Format insider trading data for Telegram
 */
function formatInsiderAlert(data) {
  const {
    ticker = 'N/A',
    filing_count = 0,
    latest_filing = 'N/A'
  } = data;

  return `
🟢 <b>Insider Trading Alert</b>

📊 <b>Ticker:</b> <code>${ticker}</code>
📋 <b>Filings (7 days):</b> ${filing_count}
📅 <b>Latest:</b> ${latest_filing}

🕐 ${new Date().toLocaleString('en-US', { timeZone: 'Europe/Warsaw' })}
  `.trim();
}

/**
 * Send insider trading alert to webhook
 */
async function sendInsiderAlert(data) {
  const WEBHOOK_URL = process.env.WEBHOOK_URL || 'http://localhost:3000/webhook/insider-trading';

  try {
    await axios.post(WEBHOOK_URL, {
      type: 'insider_trading',
      ticker: data.ticker,
      company: data.ticker,
      filing_count: data.filing_count,
      latest_filing: data.latest_filing,
      timestamp: new Date().toISOString()
    }, {
      headers: { 'Content-Type': 'application/json' }
    });

    logger.info(`Insider alert sent for ${data.ticker}`);
  } catch (error) {
    logger.error('Failed to send insider alert:', error.message);
    throw error;
  }
}

export default {
  getCIK,
  loadTickerMappings,
  getRecentForm4Filings,
  monitorTickers,
  formatInsiderAlert,
  sendInsiderAlert
};
