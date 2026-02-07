# 🚀 PEŁNA KONFIGURACJA VPS (72.61.139.13)

## 📡 TWÓJ WEBHOOK URL:

```
http://72.61.139.13:3000/webhook/tradingview
```

---

## KROK 1: SSH na VPS

```bash
ssh root@72.61.139.13
```

---

## KROK 2: Zainstaluj Docker

```bash
apt update
apt install -y docker.io docker-compose git curl
systemctl start docker
systemctl enable docker
```

---

## KROK 3: Utwórz katalog

```bash
mkdir -p ~/trading-webhook
cd ~/trading-webhook
```

---

## KROK 4: Skopiuj pliki (wybierz OPCJĘ A lub B)

### OPCJA A - Z Maca (szybsza):

Na swoim Macu uruchom:

```bash
cd ~/trading-webhook-stack

rsync -av --exclude='node_modules' \
  --exclude='.git' \
  --exclude='logs' \
  --exclude='backups' \
  --exclude='*.db' \
  ./ root@72.61.139.13:~/trading-webhook/
```

### OPCJA B - Na VPS (ręcznie):

```bash
# Utwórz package.json
cat > package.json << 'JSON'
{
  "name": "trading-webhook-stack",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "start": "node backend/server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "node-telegram-bot-api": "^0.66.0",
    "better-sqlite3": "^9.2.2",
    "dotenv": "^16.3.1",
    "winston": "^3.11.0"
  }
}
JSON

# Utwórz Dockerfile
cat > Dockerfile << 'DOCKER'
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .
RUN mkdir -p logs backups database
EXPOSE 3000
CMD ["npm", "start"]
DOCKER

# Utwórz docker-compose.yml
cat > docker-compose.yml << 'COMPOSE'
version: '3.8'
services:
  trading-webhook:
    build: .
    container_name: trading-webhook
    restart: unless-stopped
    ports:
      - "3000:3000"
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
      - ./backups:/app/backups
      - ./database:/app/database
COMPOSE
```

---

## KROK 5: Konfiguruj .env

```bash
# Utwórz .env z swoimi danymi Telegram:
cat > .env << 'ENV'
PORT=3000
NODE_ENV=production

# Telegram - WSTAW SWOJE DANE:
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789

LOG_LEVEL=info
DATABASE_PATH=./database/trading.db
ENV
```

**ZMIEŃ TOKEN I CHAT ID NA SWOJE!**

---

## KROK 6: Utwórz strukturę plików

```bash
# Utwórz foldery
mkdir -p backend/routes backend/services backend/handlers backend/utils database logs backups

# Utwórz main server
cat > backend/server.js << 'SERVER'
import express from 'express';
import dotenv from 'dotenv';
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', port: PORT });
});

// Import routes
import webhookRouter from './routes/webhook.js';
import { sendTelegramNotification } from './services/telegram.js';

app.use('/webhook', webhookRouter);

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});
SERVER

# Utwórz webhook route
cat > backend/routes/webhook.js << 'WEBHOOK'
import express from 'express';
import { sendTelegramNotification } from '../services/telegram.js';

const router = express.Router();

router.post('/tradingview', async (req, res) => {
  try {
    const data = req.body;
    console.log('Webhook received:', data);

    const signal = {
      timestamp: new Date().toISOString(),
      symbol: data.ticker || data.symbol || 'N/A',
      action: data.action || 'SIGNAL',
      price: data.price || data.close || 0,
      timeframe: data.timeframe || data.interval || 'N/A',
      strategy: data.strategy || 'TradingView',
      stop_loss: data.sl || 0,
      take_profit: data.tp || 0
    };

    await sendTelegramNotification(signal);
    res.json({ success: true, signal });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: error.message });
  }
});

export default router;
WEBHOOK

# Utwórz Telegram service
cat > backend/services/telegram.js << 'TELEGRAM'
import TelegramBot from 'node-telegram-bot-api';

let bot = null;

export async function sendTelegramNotification(signal) {
  if (!bot) {
    bot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN, { polling: false });
  }

  const chatId = process.env.TELEGRAM_CHAT_ID;

  let emoji = '⚡';
  if (signal.action?.toUpperCase() === 'LONG' || signal.action?.toUpperCase() === 'BUY') {
    emoji = '🟢';
  } else if (signal.action?.toUpperCase() === 'SHORT' || signal.action?.toUpperCase() === 'SELL') {
    emoji = '🔴';
  }

  let message = `${emoji} *Trading Signal*\n\n`;
  message += `**${signal.action}** ${signal.symbol}\n`;
  message += `💰 **Price:** ${signal.price}\n`;
  message += `⏱ **Timeframe:** ${signal.timeframe}\n`;

  if (signal.stop_loss > 0 || signal.take_profit > 0) {
    message += `🛑 **SL:** ${signal.stop_loss} | 🎯 **TP:** ${signal.take_profit}\n`;
  }

  message += `\n🕐 *${new Date(signal.timestamp).toLocaleString('pl-PL')}*`;

  await bot.sendMessage(chatId, message, { parse_mode: 'Markdown' });
}
TELEGRAM
```

---

## KROK 7: Uruchom kontener

```bash
# Zbuduj i uruchom
docker-compose up -d --build

# Sprawdź logi
docker-compose logs -f
```

---

## KROK 8: Otwórz port 3000 w firewall

```bash
ufw allow 3000/tcp
# LUB w panelu Hostinger dodaj regułę firewall
```

---

## KROK 9: Testuj

```bash
# Test health
curl http://localhost:3000/health

# Test webhook
curl -X POST http://localhost:3000/webhook/tradingview \
  -H "Content-Type: application/json" \
  -d '{"ticker":"XAUUSD","action":"LONG","price":"2345.50"}'
```

---

## KROK 10: Sprawdź z zewnątrz

W przeglądarce:
```
http://72.61.139.13:3000/health
```

Powinno zwrócić: `{"status":"ok","port":3000}`

---

## ✅ GOTOWE!

TradingView Webhook URL:
```
http://72.61.139.13:3000/webhook/tradingview
```

Message (JSON):
```json
{
  "ticker": "{{ticker}}",
  "action": "LONG",
  "price": "{{close}}",
  "timeframe": "{{interval}}"
}
```
