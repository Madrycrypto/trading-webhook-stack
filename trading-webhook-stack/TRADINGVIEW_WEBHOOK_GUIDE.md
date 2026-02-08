# 📡 TRADINGVIEW WEBHOOK - KOMPLETNY PRZEWODNIK

## 🔗 WEBHOOK URL

```
http://72.61.139.13/webhook/tradingview
```

**Bot Telegram:** `@AlertyTV_bot` (Chat ID: 641434500)

---

## 📋 SPIS TREŚCI

1. [Podstawowe formaty JSON](#podstawowe-formaty-json)
2. [Pełne formaty JSON](#pełne-formaty-json)
3. [Formaty dla HTS Strategy](#formaty-dla-hts-strategy)
4. [Formaty dla MTF Strategy](#formaty-dla-mtf-strategy)
5. [Formaty specjalne](#formaty-specjalne)
6. [Przykłady użycia](#przykłady-użycia)

---

## 1. PODSTAWOWE FORMATY JSON

### 1.1 MINIMALNY FORMAT (Najprostszy)

```json
{
  "ticker": "{{ticker}}",
  "action": "LONG",
  "price": "{{close}}"
}
```

**Użyj gdy:** Chcesz tylko podstawowe informacje

**Wynik Telegram:**
```
📊 Trading Signal
🟢 LONG XAUUSD
💰 Price: 2350.00
```

---

### 1.2 FORMAT PODSTAWOWY

```json
{
  "ticker": "{{ticker}}",
  "action": "LONG",
  "price": "{{close}}",
  "timeframe": "{{interval}}"
}
```

**Wynik Telegram:**
```
📊 Trading Signal
🟢 LONG XAUUSD
💰 Price: 2350.00
⏱ Timeframe: 15m
```

---

### 1.3 FORMAT Z SL

```json
{
  "ticker": "{{ticker}}",
  "action": "LONG",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "timeframe": "{{interval}}"
}
```

**Wynik Telegram (z automatyczną kalkulacją TP):**
```
📊 Trading Signal
🟢 LONG XAUUSD
💰 Price: 2350.00
⏱ Timeframe: 15m

🛑 SL: 2340.00
🎯 TP1 (1:1): 2360.00 (BE)
🎯 TP2 (1:2): 2370.00
🎯 TP3 (1:3): 2380.00
```

---

## 2. PEŁNE FORMATY JSON

### 2.1 PEŁNY FORMAT STANDARDOWY

```json
{
  "ticker": "{{ticker}}",
  "action": "LONG",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "timeframe": "{{interval}}",
  "strategy": "HTS Strategy",
  "setup": "MTF Alignment",
  "risk_percent": 2
}
```

**Wynik Telegram:**
```
📊 Trading Signal

🟢 LONG XAUUSD
💰 Price: 2350.00
⏱ Timeframe: 15m
📊 Indicator: HTS Strategy
📍 Setup: MTF Alignment
⚠️ Risk: 2%

🛑 SL: 2340.00
🎯 TP1 (1:1): 2360.00 (BE)
🎯 TP2 (1:2): 2370.00
🎯 TP3 (1:3): 2380.00

🕐 08.02.2025, 10:51:24
```

---

### 2.2 PEŁNY FORMAT Z NOTATKAMI

```json
{
  "ticker": "{{ticker}}",
  "action": "SHORT",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "timeframe": "{{interval}}",
  "strategy": "HTS Strategy",
  "setup": "Trend Reversal",
  "fibonacci_level": "0.618",
  "indicator_value": "RSI: 65, MACD: +0.5",
  "notes": "Silny sygnał sprzedaży, wszystkie timeframe zgodne",
  "risk_percent": 1.5
}
```

---

### 2.3 PEŁNY FORMAT Z TP RĘCZNE

```json
{
  "ticker": "{{ticker}}",
  "action": "LONG",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "tp": "{{plot_1}}",
  "timeframe": "{{interval}}",
  "strategy": "Custom Strategy"
}
```

**Uwaga:** Jeśli podasz `tp`, system NIE będzie automatycznie kalkulować TP1/TP2/TP3

---

## 3. FORMATY DLA HTS STRATEGY

### 3.1 HTS - PRZECIĘCIE WSTĘG (Crossover)

```json
{
  "ticker": "{{ticker}}",
  "action": "LONG",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "timeframe": "{{interval}}",
  "strategy": "HTS Wstęgi",
  "setup": "Fast przecina Slow wzrostowo"
}
```

**Alert condition w HTS Strategy:**
```
Add Long - przecięcie wstęg
Add Short - przecięcie wstęg
```

---

### 3.2 HTS - PIVOT POINTS

```json
{
  "ticker": "{{ticker}}",
  "action": "LONG",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "timeframe": "{{interval}}",
  "strategy": "HTS Pivot Points",
  "setup": "Odbicie od S1",
  "fibonacci_level": "S1"
}
```

**Dostępne poziomy Pivot:**
- `SL` - Stop Loss (na podstawie wstęgi)
- `TP1` - Take Profit 1 (R1)
- `TP2` - Take Profit 2 (R2)
- `TP3` - Take Profit 3 (R3)
- `S1`, `S2`, `S3` - Support levels
- `R1`, `R2`, `R3` - Resistance levels

---

### 3.3 HTS - BANDY ATR

```json
{
  "ticker": "{{ticker}}",
  "action": "LONG",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "timeframe": "{{interval}}",
  "strategy": "HTS Bandy ATR",
  "setup": "Odbicie od dolnego pasma"
}
```

**Alert conditions w ATR Bands:**
- `Bandy ATR Alert (Recommended✅)` - Główny alert
- `Bandy ATR Long` - Sygnał kupna
- `Bandy ATR Short` - Sygnał sprzedaży

---

### 3.4 HTS - KIJUN-SEN

```json
{
  "ticker": "{{ticker}}",
  "action": "LONG",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "timeframe": "{{interval}}",
  "strategy": "HTS Kijun-Sen",
  "setup": "Przebicie Kijun-Sen"
}
```

---

### 3.5 HTS - VWAP

```json
{
  "ticker": "{{ticker}}",
  "action": "LONG",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "timeframe": "{{interval}}",
  "strategy": "HTS VWAP",
  "setup": "Odbicie od VWAP"
}
```

---

### 3.6 HTS - VIDYA + TMA

```json
{
  "ticker": "{{ticker}}",
  "action": "LONG",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "timeframe": "{{interval}}",
  "strategy": "HTS VIDYA+TMA",
  "setup": "Przecięcie VIDYA/TMA"
}
```

---

### 3.7 HTS - TABELA TRENDÓW

```json
{
  "ticker": "{{ticker}}",
  "action": "LONG",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "timeframe": "{{interval}}",
  "strategy": "HTS MTF Table",
  "setup": "Wszystkie TF wzrostowe"
}
```

**Dostępne informacje z tabeli trendów:**
- Wszystkie timeframe (m1, m3, m5, m15, m30, m45, H1, H2, H3, H4, D1, W1)
- Kierunek trendu (▲ / ▼ / ■)
- Pozycja ceny względem wstęg
- Wartości RSI dla każdego TF
- Poziomy Pivot Points (Daily, Weekly)

---

## 4. FORMATY DLA MTF STRATEGY

### 4.1 MTF - STANY SYSTEMU

```json
{
  "ticker": "{{ticker}}",
  "action": "LONG",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "timeframe": "{{interval}}",
  "strategy": "MTF_v3",
  "setup": "ALL_TF_UP",
  "indicator_value": "Fast:↑ Medium:↑ Slow:↑"
}
```

**Stany systemu MTF:**
- `0` = WAIT (oczekiwanie)
- `1` = ALL ALIGN (wszystkie TF zgodne)
- `2` = CHANGE (zmiana trendu)
- `3` = LOCAL (gra lokalna)
- `4` = CLOSE (zamknij lokalne)
- `5` = NEW (nowy trend)
- `6` = STRONG (silny trend wyższego rzędu)

---

### 4.2 MTF - LONG ENTRY

```json
{
  "ticker": "{{ticker}}",
  "action": "LONG",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "timeframe": "{{interval}}",
  "strategy": "MTF_v3",
  "setup": "ALL_TF_UP"
}
```

**Kierunek:** `LONG` lub `SHORT`

---

### 4.3 MTF - NOWY TREND

```json
{
  "ticker": "{{ticker}}",
  "action": "SHORT",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "timeframe": "{{interval}}",
  "strategy": "MTF_v3",
  "setup": "NEW_Trend_DOWN",
  "notes": "Zmiana trendu z wzrostowego na spadkowy"
}
```

---

### 4.4 MTF - SILNY SYGNAŁ

```json
{
  "ticker": "{{ticker}}",
  "action": "LONG",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "timeframe": "{{interval}}",
  "strategy": "MTF_v3",
  "setup": "STRONG_UP",
  "notes": "Trend wyższego rzędu wzrostowy"
}
```

---

### 4.5 MTF - REBOUND ADD

```json
{
  "ticker": "{{ticker}}",
  "action": "LONG",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "timeframe": "{{interval}}",
  "strategy": "MTF_v3 Rebound",
  "setup": "Rebound ADD",
  "notes": "Odbicie od strefy SL, dobranie do pozycji"
}
```

---

### 4.6 MTF - WEEKEND CLOSE

```json
{
  "ticker": "{{ticker}}",
  "action": "CLOSE",
  "price": "{{close}}",
  "timeframe": "{{interval}}",
  "strategy": "MTF_v3",
  "setup": "Weekend Close",
  "notes": "Automatyczne zamknięcie przed weekendem"
}
```

---

## 5. FORMATY SPECJALNE

### 5.1 SIGNAL BEZ SL (tylko informacyjny)

```json
{
  "ticker": "{{ticker}}",
  "action": "SIGNAL",
  "price": "{{close}}",
  "timeframe": "{{interval}}",
  "strategy": "Monitorowanie",
  "notes": "Potencjalna okazja, czekaj na potwierdzenie"
}
```

**Wynik Telegram:**
```
⚡ Trading Signal
📊 SIGNAL XAUUSD
💰 Price: 2350.00
⏱ Timeframe: 15m
📊 Indicator: Monitorowanie
📝 Notes: Potencjalna okazja, czekaj na potwierdzenie
```

---

### 5.2 POZYCJA ZAMYKANA

```json
{
  "ticker": "{{ticker}}",
  "action": "CLOSE",
  "price": "{{close}}",
  "timeframe": "{{interval}}",
  "strategy": "MTF_v3",
  "setup": "TP1 Hit",
  "notes": "Zamknięto 50% pozycji na TP1"
}
```

---

### 5.3 ALERT O BŁĘDZIE/OSTRZEŻENIE

```json
{
  "ticker": "{{ticker}}",
  "action": "WARNING",
  "price": "{{close}}",
  "timeframe": "{{interval}}",
  "strategy": "System",
  "notes": "Daily limit osiągnięty - zatrzymano trading"
}
```

---

### 5.4 CUSTOM MESSAGE

```json
{
  "ticker": "{{ticker}}",
  "action": "INFO",
  "price": "{{close}}",
  "timeframe": "{{interval}}",
  "strategy": "Custom",
  "notes": "Twoja własna wiadomość"
}
```

---

## 6. PRZYKŁADY UŻYCIA

### 6.1 TRADINGVIEW ALERT SETUP

#### Krok 1: Otwórz Alert w TradingView
1. Kliknij przycisk "Alert" na górnym pasku
2. Wybierz warunek alertu

#### Krok 2: Wybierz Condition
**Dla HTS Wstęgi:**
- `Add Long - przecięcie wstęg`
- `Add Short - przecięcie wstęg`

**Dla MTF Strategy:**
- Użyj wbudowanych alertów z kodu Pine Script

#### Krok 3: Wpisz Message (JSON)

**Przykład 1 - Podstawowy:**
```json
{
  "ticker": "{{ticker}}",
  "action": "LONG",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "timeframe": "{{interval}}",
  "strategy": "HTS Wstęgi"
}
```

**Przykład 2 - Pełny:**
```json
{
  "ticker": "{{ticker}}",
  "action": "{{strategy.order.action}}",
  "price": "{{close}}",
  "sl": "{{plot_0}}",
  "timeframe": "{{interval}}",
  "strategy": "HTS Strategy",
  "setup": "Crossover Signal"
}
```

#### Krok 4: Wpisz Webhook URL
```
http://72.61.139.13/webhook/tradingview
```

#### Krok 5: Ustawienia (opcjonalnie)
- **Only once per bar close:** TAK (zalecane)
- **Trigger:** Once Per Bar Close

---

### 6.2 ZMIENNE TRADINGVIEW

#### Podstawowe zmienne:
| Zmienna | Opis | Przykład |
|---------|------|---------|
| `{{ticker}}` | Symbol instrumentu | `XAUUSD` |
| `{{close}}` | Cena zamknięcia | `2350.50` |
| `{{open}}` | Cena otwarcia | `2348.00` |
| `{{high}}` | Najwyższa cena | `2355.00` |
| `{{low}}` | Najniższa cena | `2345.00` |
| `{{interval}}` | Interwał czasowy | `15`, `60`, `D` |
| `{{time}}` | Timestamp | `1704729600` |
| `{{timenow}}` | Aktualny czas (tekst) | `2024-01-08 15:30:00` |

#### Zaawansowane zmienne:
| Zmienna | Opis |
|---------|------|
| `{{plot_0}}` | Wartość plotu 0 |
| `{{plot_1}}` | Wartość plotu 1 |
| `{{strategy.order.action}}` | Akcja strategii (buy/sell) |
| `{{strategy.order.contracts}}` | Liczba kontraktów |
| `{{strategy.order.price}}` | Cena zlecenia |
| `{{strategy.position_size}}` | Rozmiar pozycji |
| `{{strategy.market_position}}` | Pozycja (long/short/flat) |

---

### 6.3 DOSTĘPNE WPRAWY (ACTIONS)

| Action | Emoji | Opis |
|--------|-------|------|
| `LONG` | 🟢 | Sygnał kupna |
| `BUY` | 🟢 | Sygnał kupna (alternatywa) |
| `SHORT` | 🔴 | Sygnał sprzedaży |
| `SELL` | 🔴 | Sygnał sprzedaży (alternatywa) |
| `SIGNAL` | ⚡ | Sygnał neutralny |
| `CLOSE` | ⏹️ | Zamknięcie pozycji |
| `INFO` | ℹ️ | Informacja |
| `WARNING` | ⚠️ | Ostrzeżenie |

---

### 6.4 POLA DOSTĘPNE W JSON

| Pole | Wymagane | Typ | Opis |
|-----|----------|-----|------|
| `ticker` | ❌ | string | Symbol (domyślnie z {{ticker}}) |
| `action` | ✅ | string | Typ sygnału (LONG/SHORT/SIGNAL/...) |
| `price` | ❌ | number | Cena (domyślnie z {{close}}) |
| `sl` | ❌ | number | Stop Loss |
| `tp` | ❌ | number | Take Profit (ręczny) |
| `timeframe` | ❌ | string | Interwał |
| `strategy` | ❌ | string | Nazwa strategii/indytora |
| `setup` | ❌ | string | Opis setupu |
| `fibonacci_level` | ❌ | string | Poziom Fibonacciego |
| `indicator_value` | ❌ | string | Wartość indytora |
| `notes` | ❌ | string | Dodatkowe notatki |
| `risk_percent` | ❌ | number | Ryzyko w % |

---

## 7. PRZYKŁADOWY KOD PINE SCRIPT

### 7.1 Dodanie alertu w HTS Strategy

```pinescript
// Na końcu kodu HTS Strategy
alertcondition(uptrendCrossover,
     title = 'HTS Long Signal',
     message = '{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"HTS Wstęgi"}')

alertcondition(downtrendCrossunder,
     title = 'HTS Short Signal',
     message = '{"ticker":"{{ticker}}","action":"SHORT","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"HTS Wstęgi"}')
```

---

## 8. TROUBLESHOOTING

### Problem: Nie otrzymuję wiadomości Telegram

**Rozwiązania:**
1. Sprawdź czy Webhook URL jest poprawny: `http://72.61.139.13/webhook/tradingview`
2. Sprawdź czy JSON jest poprawny (użyj JSON validator)
3. Sprawdź czy alert jest włączony w TradingView
4. Sprawdź czy bot `@AlertyTV_bot` nie jest zablokowany

### Problem: TP1/TP2/TP3 nie są kalkulowane

**Rozwiązanie:**
Upewnij się że pole `sl` jest obecne w JSON i ma wartość liczbową:

```json
{
  "sl": "{{plot_0}}"  // ✅ poprawnie
}
```

```json
{
  "sl": "N/A"  // ❌ błędnie - nie kalkuluje TP
}
```

---

## 9. AUTOMATYCZNA KALKULACJA TP

System automatycznie oblicza TP1/TP2/TP3 gdy podany jest SL:

**Dla LONG:**
- TP1 (1:1) = Entry + (Entry - SL)
- TP2 (1:2) = Entry + 2×(Entry - SL)
- TP3 (1:3) = Entry + 3×(Entry - SL)

**Dla SHORT:**
- TP1 (1:1) = Entry - (SL - Entry)
- TP2 (1:2) = Entry - 2×(SL - Entry)
- TP3 (1:3) = Entry - 3×(SL - Entry)

---

## 10. GOTOWE SZABLONY

### Szablon 1 - HTS Wstęgi (Crossover)
```
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"HTS Wstęgi","setup":"Crossover"}
```

### Szablon 2 - MTF Strategy
```
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"MTF_v3","setup":"ALL_TF_UP"}
```

### Szablon 3 - Pivot Points
```
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"Pivot Points","setup":"Odbicie od S1"}
```

### Szablon 4 - ATR Bands
```
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"ATR Bands","setup":"Odbicie od pasma"}
```

### Szablon 5 - Pełny
```
{"ticker":"{{ticker}}","action":"LONG","price":"{{close}}","sl":"{{plot_0}}","timeframe":"{{interval}}","strategy":"HTS","setup":"Sygnał","notes":"Potwierdzony na wszystkich TF","risk_percent":2}
```

---

## 11. KONTAKT I SUPPORT

**VPS Status:** http://72.61.139.13/health
**Telegram Bot:** @AlertyTV_bot
**Webhook URL:** http://72.61.139.13/webhook/tradingview

---

© 2025 Trading Webhook System | Wersja: 2.0
