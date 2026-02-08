import Database from 'better-sqlite3';
import path from 'path';
import { logger } from '../backend/utils/logger.js';

const dbPath = path.join(process.cwd(), 'database', 'trading.db');
let db;

export function initDatabase() {
  db = new Database(dbPath);

  // Enable foreign keys
  db.pragma('foreign_keys = ON');

  // Create tables
  createTables();

  logger.info(`Database initialized: ${dbPath}`);
  return db;
}

function createTables() {
  // Signals table
  db.exec(`
    CREATE TABLE IF NOT EXISTS signals (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      timestamp TEXT NOT NULL,
      symbol TEXT NOT NULL,
      action TEXT NOT NULL,
      price REAL NOT NULL,
      timeframe TEXT,
      strategy TEXT,
      type TEXT,
      setup TEXT,
      fibonacci_level TEXT,
      stop_loss REAL DEFAULT 0,
      take_profit REAL DEFAULT 0,
      risk_percent REAL DEFAULT 0,
      notes TEXT,
      indicator_value TEXT,
      raw_data TEXT,
      status TEXT DEFAULT 'pending',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Migration: Add indicator_value column if it doesn't exist
  try {
    db.exec(`ALTER TABLE signals ADD COLUMN indicator_value TEXT`);
  } catch (e) {
    // Column already exists, ignore error
  }

  // Trades table
  db.exec(`
    CREATE TABLE IF NOT EXISTS trades (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      signal_id INTEGER,
      entry_price REAL,
      exit_price REAL,
      profit_loss REAL,
      status TEXT DEFAULT 'open',
      opened_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      closed_at DATETIME,
      notes TEXT,
      FOREIGN KEY (signal_id) REFERENCES signals(id)
    )
  `);

  // Statistics table
  db.exec(`
    CREATE TABLE IF NOT EXISTS statistics (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      date TEXT NOT NULL UNIQUE,
      total_signals INTEGER DEFAULT 0,
      long_signals INTEGER DEFAULT 0,
      short_signals INTEGER DEFAULT 0,
      won_trades INTEGER DEFAULT 0,
      lost_trades INTEGER DEFAULT 0,
      total_profit REAL DEFAULT 0,
      total_loss REAL DEFAULT 0,
      win_rate REAL DEFAULT 0,
      profit_factor REAL DEFAULT 0,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Create indexes
  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_signals_timestamp ON signals(timestamp);
    CREATE INDEX IF NOT EXISTS idx_signals_symbol ON signals(symbol);
    CREATE INDEX IF NOT EXISTS idx_signals_type ON signals(type);
    CREATE INDEX IF NOT EXISTS idx_trades_signal_id ON trades(signal_id);
  `);

  logger.info('Database tables created');
}

// Signal operations
export async function saveSignal(signal) {
  const stmt = db.prepare(`
    INSERT INTO signals (
      timestamp, symbol, action, price, timeframe, strategy, type,
      setup, fibonacci_level, stop_loss, take_profit, risk_percent,
      notes, indicator_value, raw_data
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `);

  const result = stmt.run(
    signal.timestamp,
    signal.symbol,
    signal.action,
    signal.price,
    signal.timeframe,
    signal.strategy,
    signal.type,
    signal.setup,
    signal.fibonacci_level,
    signal.stop_loss,
    signal.take_profit,
    signal.risk_percent,
    signal.notes,
    signal.indicator_value || null,
    signal.raw_data
  );

  return result.lastInsertRowid;
}

export async function getSignalsPaginated(page = 1, limit = 50) {
  const offset = (page - 1) * limit;
  const signals = db.prepare(`
    SELECT * FROM signals
    ORDER BY timestamp DESC
    LIMIT ? OFFSET ?
  `).all(limit, offset);

  const total = db.prepare('SELECT COUNT(*) as count FROM signals').get();

  return {
    signals,
    pagination: {
      page,
      limit,
      total: total.count,
      pages: Math.ceil(total.count / limit)
    }
  };
}

export async function getSignal(id) {
  return db.prepare('SELECT * FROM signals WHERE id = ?').get(id);
}

export async function getSignalsByDate(date) {
  return db.prepare(`
    SELECT * FROM signals
    WHERE DATE(timestamp) = ?
    ORDER BY timestamp DESC
  `).all(date);
}

export async function getSignalsByType(type) {
  return db.prepare(`
    SELECT * FROM signals
    WHERE type = ?
    ORDER BY timestamp DESC
  `).all(type);
}

// Statistics operations
export async function getTotalSignals() {
  const result = db.prepare('SELECT COUNT(*) as count FROM signals').get();
  return result.count;
}

export async function getTodaySignals() {
  const today = new Date().toISOString().split('T')[0];
  const result = db.prepare(`
    SELECT COUNT(*) as count FROM signals
    WHERE DATE(timestamp) = ?
  `).get(today);
  return result.count;
}

export async function getRecentSignals(limit = 10) {
  return db.prepare(`
    SELECT * FROM signals
    ORDER BY timestamp DESC
    LIMIT ?
  `).all(limit);
}

export async function getStatsByType() {
  return db.prepare(`
    SELECT
      type,
      COUNT(*) as count,
      AVG(price) as avg_price
    FROM signals
    GROUP BY type
  `).all();
}

export async function getWinRate() {
  const won = db.prepare("SELECT COUNT(*) as count FROM trades WHERE status = 'won'").get();
  const total = db.prepare("SELECT COUNT(*) as count FROM trades WHERE status IN ('won', 'lost')").get();

  if (total.count === 0) return 0;
  return ((won.count / total.count) * 100).toFixed(2);
}

export async function getProfitFactor() {
  const profit = db.prepare("SELECT SUM(profit_loss) as total FROM trades WHERE status = 'won'").get();
  const loss = db.prepare("SELECT SUM(ABS(profit_loss)) as total FROM trades WHERE status = 'lost'").get();

  if (!loss.total || loss.total === 0) return profit.total || 0;
  return (profit.total / loss.total).toFixed(2);
}

export async function getDailyStatistics(date) {
  const signals = db.prepare(`
    SELECT COUNT(*) as count FROM signals
    WHERE DATE(timestamp) = ?
  `).get(date);

  const long = db.prepare(`
    SELECT COUNT(*) as count FROM signals
    WHERE DATE(timestamp) = ? AND action = 'LONG'
  `).get(date);

  const short = db.prepare(`
    SELECT COUNT(*) as count FROM signals
    WHERE DATE(timestamp) = ? AND action = 'SHORT'
  `).get(date);

  return {
    date,
    totalSignals: signals.count,
    longSignals: long.count,
    shortSignals: short.count
  };
}

export async function getMonthlyStatistics(month) {
  const signals = db.prepare(`
    SELECT COUNT(*) as count FROM signals
    WHERE strftime('%Y-%m', timestamp) = ?
  `).get(month);

  const byDay = db.prepare(`
    SELECT
      DATE(timestamp) as day,
      COUNT(*) as count,
      SUM(CASE WHEN action = 'LONG' THEN 1 ELSE 0 END) as longs,
      SUM(CASE WHEN action = 'SHORT' THEN 1 ELSE 0 END) as shorts
    FROM signals
    WHERE strftime('%Y-%m', timestamp) = ?
    GROUP BY DATE(timestamp)
    ORDER BY day
  `).all(month);

  return {
    month,
    totalSignals: signals.count,
    dailyBreakdown: byDay
  };
}

export function closeDatabase() {
  if (db) {
    db.close();
    logger.info('Database closed');
  }
}
