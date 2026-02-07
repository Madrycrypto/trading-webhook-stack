#!/usr/bin/env node
/**
 * Test script for insider trading scrapers
 * Run: node scrapers/test.js
 */

import axios from 'axios';

const WEBHOOK_URL = process.env.WEBHOOK_URL || 'http://localhost:3000/webhook/insider-trading';

// Test data
const testFiling = {
  type: 'insider_trading',
  ticker: 'AAPL',
  company: 'Apple Inc.',
  insider: 'Test Executive',
  transaction: 'Purchase',
  shares: '1,000',
  price: '$180.50',
  value: '$180,500',
  filing_date: '2025-02-07',
  url: 'https://www.sec.gov/test',
  timestamp: new Date().toISOString()
};

async function testWebhook() {
  console.log('🧪 Testing Insider Trading Webhook...\n');

  try {
    // Test health endpoint
    console.log('1. Checking webhook server health...');
    const healthResponse = await axios.get('http://localhost:3000/health');
    console.log('   ✓ Server is running:', healthResponse.data.status);
    console.log('   ✓ Timestamp:', healthResponse.data.timestamp);

    // Test webhook endpoint
    console.log('\n2. Sending test filing to webhook...');
    const webhookResponse = await axios.post(WEBHOOK_URL, testFiling, {
      headers: { 'Content-Type': 'application/json' }
    });

    console.log('   ✓ Webhook responded:', webhookResponse.status);
    console.log('   ✓ Response:', webhookResponse.data);

    console.log('\n✅ All tests passed!\n');
    console.log('Your webhook endpoint is ready to receive insider trading data.');
    console.log('Start the scraper with:');
    console.log('  python scrapers/sec_monitor.py --once');
    console.log('  node scrapers/index.js --once');

  } catch (error) {
    if (error.code === 'ECONNREFUSED') {
      console.error('\n❌ Error: Webhook server is not running!');
      console.error('\nStart the server first:');
      console.error('  npm start\n');
    } else {
      console.error('\n❌ Error:', error.message);
      if (error.response) {
        console.error('Response:', error.response.data);
      }
    }
    process.exit(1);
  }
}

// Run tests
testWebhook();
