# 🔍 Wyszukiwarka Workflowów N8N

Aplikacja do wyszukiwania i przeglądania **448 workflowów N8N** z podziałem na kategorie po polsku.

## 📊 Statystyki

| Kategoria | Liczba Workflowów |
|-----------|-------------------|
| Automatyzacja | 252 |
| Integracja Danych | 75 |
| Komunikacja | 41 |
| Przetwarzanie Dokumentów | 30 |
| Transformacja Danych | 24 |
| API i Webhooki | 20 |
| Analityka | 6 |
| **RAZEM** | **448** |

## 🚀 Szybki Start

### 1. Uruchomienie serwera:

```bash
cd ~/trading-webhook-stack
node n8n-search-server.js
```

Serwer będzie działał na: **http://localhost:3001**

### 2. Otwórz w przeglądarce:

```
http://localhost:3001
```

## 🔎 Funkcje Wyszukiwarki

### Szybkie wyszukiwanie:
- Wpisz słowo kluczowe (np. "slack", "email", "telegram")
- Wyniki pojawiają się na żywo

### Filtry kategorii:
- Kliknij na kategorię aby przefiltrować
- Kategorie po polsku dla łatwiejszego nawigowania

### Podgląd workflow:
- Kliknij na kartę aby zobaczyć szczegóły
- Zobacz użyte node'y i opis

## 📁 Pliki

| Plik | Opis |
|------|------|
| `n8n-search.html` | Interfejs webowy |
| `n8n-search-server.js` | Serwer API (Express) |
| `n8n_workflows.db` | Baza danych SQLite |
| `n8n_workflows_index.json` | Indeks workflowów |

## 🔗 API Endpointy

### Pobierz wszystkie workflowy:
```bash
curl http://localhost:3001/api/workflows
```

### Szukaj po słowie kluczowym:
```bash
curl "http://localhost:3001/api/workflows/search?q=slack"
```

### Filtruj po kategorii:
```bash
curl "http://localhost:3001/api/workflows/search?category=Komunikacja"
```

### Pobierz workflow po ID:
```bash
curl http://localhost:3001/api/workflows/1690-markdown-report-generation
```

## 📂 Źródło Workflowów

Workflowy pochodzą z:
```
~/Desktop/4000+ N8N Workflow Automation Templates By ExclusiveTechAccess/
```

## 🛠️ Technologie

- **Node.js** + Express
- **SQLite** (better-sqlite3)
- **HTML/CSS** + Vanilla JavaScript
- **Python** (skrypt indeksujący)

## 🔄 Odświeżenie Danych

Jeśli dodasz nowe workflowy, uruchom:

```bash
cd ~/trading-webhook-stack
python3 << 'EOF'
# Skrypt indeksujący (zobacz powyższą konwersację)
EOF
```

## 📝 Kategorie (Polski -> Angielski)

| Polski | Angielski |
|--------|-----------|
| AI - Badania, RAG i Analiza Danych | AI_Research_RAG_and_Data_Analysis |
| Analityka | analytics |
| API i Webhooki | api-webhooks |
| Automatyzacja | automation |
| Bazy Danych i Przechowywanie | Database_and_Storage |
| Discord | Discord |
| Gmail i Automatyzacja Email | Gmail_and_Email_Automation |
| Google Drive i Sheets | Google_Drive_and_Google_Sheets |
| HR i Rekrutacja | HR_and_Recruitment |
| Inne | Other |
| Inne Integracje i Przypadki Użycia | Other_Integrations_and_Use_Cases |
| Integracja Danych | data-integration |
| Komunikacja | communication |
| Notion | Notion |
| PDF i Przetwarzanie Dokumentów | PDF_and_Document_Processing |
| Przetwarzanie Dokumentów | document-processing |
| Slack | Slack |
| Social Media | Instagram_Twitter_Social_Media |
| Telegram | Telegram |
| Transformacja Danych | data-transformation |
| WhatsApp | WhatsApp |
| WordPress | WordPress |

## 🎨 Przykłady Wyszukiwań

### "email" - 33 wyniki:
- Send Notification When Deployment Fails
- Report N8N Workflow Errors Directly To Your Email
- Send An Email Template Using Mandrill

### "slack" - 30 wyników:
- Advanced Slackbot With N8N
- Report N8N Workflow Errors To Slack
- Share YouTube Videos with AI Summaries on Discord

### "telegram" - 21 wyników:
- Send Automated Daily Reminders On Telegram
- Send New Youtube Channel Videos To Telegram
- Get Data From Multiple Rss Feeds To Telegram

---

**Gotowe do użycia! 🎉**
