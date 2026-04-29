# Multi-Agent System

Ein vollständiges Multi-Agent-System mit Coder-Agent, Reviewer-Agent, Orchestrator, Discord Bot und Streamlit Dashboard.

## Setup

1. Python 3.10+ installieren.
2. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
3. Environment Variablen setzen:
   ```bash
   cp .env.example .env
   ```
   Dann `.env` ausfüllen:
   - `OPENAI_API_KEY`
   - `DISCORD_BOT_TOKEN`
   - `CODER_MODEL` (default: `gpt-4.1`)
   - `REVIEWER_MODEL` (default: `gpt-4o-mini`)

## Model-Konfiguration (Railway)

In Railway unter **Variables** kannst du die Agent-Modelle ohne Codeänderung steuern:

- `CODER_MODEL` für den Coder-Agent
- `REVIEWER_MODEL` für den Reviewer-Agent

Wenn Variablen nicht gesetzt sind, nutzt das System automatisch:
- Coder: `gpt-4.1`
- Reviewer: `gpt-4o-mini`

## Start

### Discord Bot starten
```bash
python discord_bot/bot.py
```

### Dashboard starten
```bash
streamlit run dashboard/dashboard.py
```

### Workflow lokal testen
```bash
python main.py
```

## Discord Commands

- `!task <beschreibung>`: Startet den Multi-Agent-Workflow (Coder -> Reviewer -> ggf. zweiter Durchlauf).
