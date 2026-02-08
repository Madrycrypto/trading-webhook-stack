# 📝 TRADINGVIEW WEBHOOK - PRZYKŁADY JSON

## WEBHOOK URL
```
http://72.61.139.13/webhook/tradingview
```

---

## 1. PODSTAWOWE PRZYKŁADY

### 1.1 Minimalny (tylko symbol i akcja)
```json
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}"}
```

### 1.2 Z timeframe
```json
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","timeframe":"{{interval}}"}
```

### 1.3 Ze SL (automatycznie kalkuluje TP1/TP2/TP3)
```json
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}"}
```

---

## 2. HTS WSTĘGI - PRZECIĘCIA

### 2.1 HTS Long Signal
```json
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"HTS Wstęgi","setup":"Fast przecina Slow"}
```

### 2.2 HTS Short Signal
```json
{"ticker":"{{ticker}}","action":"SHORT","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"HTS Wstęgi","setup":"Fast przecina Slow"}
```

### 2.3 HTS Long (z R:R)
```json
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"HTS Wstęgi","setup":"Crossover","risk_percent":2}
```

---

## 3. PIVOT POINTS

### 3.1 Odbicie od S1 (Support)
```json
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"Pivot Points","setup":"Odbicie od S1","fibonacci_level":"S1"}
```

### 3.2 Odbicie od R1 (Resistance)
```json
{"ticker":"{{ticker}}","action":"SHORT","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"Pivot Points","setup":"Odbicie od R1","fibonacci_level":"R1"}
```

### 3.3 Pivot Breakout
```json
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"Pivot Points","setup":"Breakout R1","fibonacci_level":"R1","notes":"Przebicie R1 z wolumenem"}
```

---

## 4. MTF STRATEGY

### 4.1 MTF ALL TF UP (Wszystkie timeframe zgodne)
```json
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"MTF_v3","setup":"ALL_TF_UP"}
```

### 4.2 MTF NEW TREND
```json
{"ticker":"{{ticker}}","action":"SHORT","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"MTF_v3","setup":"NEW_Trend_DOWN"}
```

### 4.3 MTF STRONG SIGNAL
```json
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"MTF_v3","setup":"STRONG_UP","notes":"Trend wyższego rzędu"}
```

### 4.4 MTF LOCAL TREND
```json
{"ticker":"{{ticker}}","action":"SHORT","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"MTF_v3","setup":"LOCAL_DOWN","notes":"Gra lokalna przeciwko trendu"}
```

### 4.5 MTF REBOUND ADD
```json
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"MTF_v3","setup":"Rebound ADD","notes":"Dobranie przy odbiciu od SL"}
```

---

## 5. BANDY ATR

### 5.1 ATR Long Signal
```json
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"ATR Bands","setup":"Odbicie od dolnego pasma"}
```

### 5.2 ATR Short Signal
```json
{"ticker":"{{ticker}}","action":"SHORT","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"ATR Bands","setup":"Odbicie od górnego pasma"}
```

---

## 6. KIJUN-SEN

### 6.1 Kijun-Sen Breakout
```json
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"Kijun-Sen","setup":"Przebicie linii"}
```

---

## 7. VWAP

### 7.1 VWAP Rebound
```json
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"VWAP","setup":"Odbicie od VWAP"}
```

### 7.2 VWAP Cross
```json
{"ticker":"{{ticker}}","action":"SHORT","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"VWAP","setup":"Przecięcie VWAP w dół"}
```

---

## 8. VIDYA + TMA

### 8.1 VIDYA/TMA Cross
```json
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"VIDYA+TMA","setup":"Przecięcie wzrostowe"}
```

---

## 9. TABELA TRENDÓW (HTS MTF)

### 9.1 Wszystkie TF zgodne
```json
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"HTS MTF Table","setup":"All TF Up","indicator_value":"m5:↑ m15:↑ H1:↑ H4:↑ D1:↑"}
```

### 9.2 Zmiana trendu
```json
{"ticker":"{{ticker}}","action":"SHORT","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"HTS MTF Table","setup":"Trend Change","indicator_value":"m5:↓ m15:↑ H1:↑"}
```

---

## 10. SYGNAŁY SPECJALNE

### 10.1 Signal bez SL (tylko informacyjny)
```json
{"ticker":"{{ticker}}","action":"SIGNAL","price":"{{close}}","timeframe":"{{interval}}","strategy":"Monitor","notes":"Potencjalna okazja"}
```

### 10.2 Close Position
```json
{"ticker":"{{ticker}}","action":"CLOSE","price":"{{close}}","timeframe":"{{interval}}","strategy":"Manual","notes":"Zamknij pozycję"}
```

### 10.3 Warning
```json
{"ticker":"{{ticker}}","action":"WARNING","price":"{{close}}","timeframe":"{{interval}}","strategy":"System","notes":"Daily limit osiągnięty"}
```

### 10.4 Info
```json
{"ticker":"{{ticker}}","action":"INFO","price":"{{close}}","timeframe":"{{interval}}","strategy":"Custom","notes":"Twoja wiadomość"}
```

---

## 11. PEŁNE PRZYKŁADY Z Wszystkimi POLAMI

### 11.1 Pełny Long Signal
```json
{
  "ticker": "{{ticker}}",
  "action": "LONG",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "timeframe": "{{interval}}",
  "strategy": "HTS Strategy",
  "setup": "MTF Alignment",
  "fibonacci_level": "0.618",
  "indicator_value": "RSI: 55, MACD: +0.3",
  "notes": "Silny sygnał, wszystkie TF zgodne",
  "risk_percent": 2
}
```

### 11.2 Pełny Short Signal
```json
{
  "ticker": "{{ticker}}",
  "action": "SHORT",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "timeframe": "{{interval}}",
  "strategy": "MTF_v3",
  "setup": "NEW_Trend_DOWN",
  "fibonacci_level": "R1",
  "indicator_value": "Fast:↓ Medium:↓ Slow:↓",
  "notes": "Zmiana trendu, pierwsza krótka",
  "risk_percent": 1.5
}
```

---

## 12. PRZYKŁADY DLA RÓŻNYCH AKTYWÓW

### 12.1 GOLD (XAUUSD)
```json
{"ticker":"XAUUSD","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"HTS Gold","setup":"HTF Trend Up"}
```

### 12.2 FOREX (EURUSD)
```json
{"ticker":"EURUSD","action":"SHORT","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"HTS Forex","setup":"D1 Trend Down"}
```

### 12.3 CRYPTO (BTCUSD)
```json
{"ticker":"BTCUSD","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"HTS Crypto","setup":"Breakout"}
```

### 12.4 INDICES (SPX500)
```json
{"ticker":"SPX500","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"HTS Indices","setup":"ATH Breakout"}
```

---

## 13. GOTOWE TEMPLATES DO SKOPIOWANIA

### Template 1 - Basic Long
```
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}"}
```

### Template 2 - Basic Short
```
{"ticker":"{{ticker}}","action":"SHORT","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}"}
```

### Template 3 - With Strategy
```
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"HTS"}
```

### Template 4 - Full Info
```
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"HTS","setup":"Signal","notes":"Notes"}
```

### Template 5 - With Risk
```
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"HTS","risk_percent":2}
```

---

## 14. TRADINGVIEW ALERTCONDITION W PINE SCRIPT

### 14.1 Dodanie alertu do HTS Strategy

Na końcu kodu HTS Strategy dodaj:

```pinescript
// Alerty dla webhook
alertcondition(uptrendCrossover,
     title = '🟢 HTS Long Webhook',
     message = '{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"HTS Wstęgi","setup":"Crossover"}')

alertcondition(downtrendCrossunder,
     title = '🔴 HTS Short Webhook',
     message = '{"ticker":"{{ticker}}","action":"SHORT","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"HTS Wstęgi","setup":"Crossover"}')
```

### 14.2 ATR Bands Alerts

```pinescript
alertcondition(alertup_atr,
     title = '📈 ATR Long Webhook',
     message = '{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"ATR Bands","setup":"Lower Band Rebound"}')

alertcondition(alertdown_atr,
     title = '📉 ATR Short Webhook',
     message = '{"ticker":"{{ticker}}","action":"SHORT","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"ATR Bands","setup":"Upper Band Rebound"}')
```

### 14.3 VWAP Cross Alert

```pinescript
alertcondition(ta.cross(close, vwapValue),
     title = '🔄 VWAP Cross Webhook',
     message = '{"ticker":"{{ticker}}","action":"SIGNAL","price":"{{close}}","timeframe":"{{interval}}","strategy":"VWAP","setup":"Price Cross VWAP"}')
```

---

## 15. OPISY SYGNAŁÓW DLA POLE "SETUP"

| Setup | Opis |
|-------|------|
| `Crossover` | Przecięcie średnich |
| `Breakout` | Przebicie poziomu |
| `Rebound` | Odbicie od poziomu |
| `ALL_TF_UP` | Wszystkie TF wzrostowe |
| `ALL_TF_DOWN` | Wszystkie TF spadkowe |
| `NEW_Trend_UP` | Nowy trend wzrostowy |
| `NEW_Trend_DOWN` | Nowy trend spadkowy |
| `STRONG_UP` | Silny trend wzrostowy |
| `STRONG_DOWN` | Silny trend spadkowy |
| `LOCAL_UP` | Lokalny trend wzrostowy |
| `LOCAL_DOWN` | Lokalny trend spadkowy |
| `Rebound ADD` | Dobranie do pozycji |
| `Weekend Close` | Zamknięcie przed weekendem |

---

## 16. TYPY AKCJI (ACTION)

| Action | Emoji | Użycie |
|--------|-------|--------|
| `LONG` | 🟢 | Sygnał kupna |
| `BUY` | 🟢 | Alternatywa dla LONG |
| `SHORT` | 🔴 | Sygnał sprzedaży |
| `SELL` | 🔴 | Alternatywa dla SHORT |
| `SIGNAL` | ⚡ | Sygnał neutralny |
| `CLOSE` | ⏹️ | Zamknij pozycję |
| `INFO` | ℹ️ | Informacja |
| `WARNING` | ⚠️ | Ostrzeżenie |

---

© 2025 Trading Webhook System
