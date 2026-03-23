# RAFI: Autonomous SQL Analyst

A professional AI-driven data analyst built with **n8n orchestration**, **FastAPI/DuckDB backend**, and a modern **web UI**. RAFI autonomously analyzes data, executes SQL queries, and delivers insights in Hebrew.

## 🚀 Features

- **Autonomous SQL Analysis**: AI agent that generates and executes SQL queries without human intervention
- **Multi-Model Support**: Gemini 2.5 Flash, GPT-4, Claude (via OpenRouter)
- **Real-time Chat Interface**: Dark-mode responsive web UI with file upload capabilities
- **CSV Data Management**: Upload and manage data with automatic schema detection
- **Hebrew Localization**: Natural language responses in Hebrew
- **Docker-Friendly**: Cross-container communication support

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (index.html)                     │
│              Modern Chat UI + Model Selector                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                   n8n Workflows                              │
│  ┌──────────────────┬──────────────────────────────────────┐│
│  │  Rafi Agent      │  Workflow SQL                        ││
│  │  (LLM + Tools)   │  (DuckDB Query Executor)             ││
│  └──────────────────┴──────────────────────────────────────┘│
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ↓                         ↓
┌──────────────────┐    ┌──────────────────┐
│  FastAPI (8001)  │    │  FastAPI (8000)  │
│  SQL Query API   │    │  CSV Upload API  │
└────────┬─────────┘    └────────┬─────────┘
         │                       │
         └───────────┬───────────┘
                     ↓
         ┌──────────────────────┐
         │   DuckDB Database    │
         │  (my_database.duckdb)│
         │   - users table      │
         │   - Live data        │
         └──────────────────────┘
```

## 📋 Prerequisites

- **Python** 3.10 or higher
- **n8n** (via Docker recommended)
- **Docker** & **Docker Compose** (for orchestration)
- **pip** (Python package manager)
- **OpenRouter API Key** (for LLM access)

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/amitnahum18/Data_Analyst_Agent.git
cd Data_Analyst_Agent
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add:
```
OPENROUTER_API_KEY=your_key_here
N8N_WEBHOOK_URL=http://localhost:5678/webhook/your-webhook-id
```

### 5. Start FastAPI Servers

**Terminal 1** - SQL Query API (Port 8001):
```bash
python SQL_query.py
```

**Terminal 2** - CSV Upload API (Port 8000):
```bash
python Update_DB.py
```

### 6. Import n8n Workflows

1. Open n8n: `http://localhost:5678`
2. Import `workflow_SQL.json` and `Rafi_Agent.json`
3. Configure credentials (OpenRouter API Key)
4. Deploy workflows

### 7. Access the Chat Interface

Open `index.html` in your browser or deploy via GitHub Pages (see below).

## 📄 GitHub Pages Deployment

To host the chat interface on GitHub Pages:

### Option A: Deploy from `/docs` folder

1. **Move `index.html` to `/docs`:**
   ```bash
   mkdir docs
   mv index.html docs/
   ```

2. **Repository Settings:**
   - Go to Settings → Pages
   - Select "Deploy from a branch"
   - Choose branch: `main`
   - Folder: `/docs`

3. **Access at:** `https://amitnahum18.github.io/Data_Analyst_Agent/`

### Option B: Deploy from root (Using gh-pages branch)

1. **Create and checkout gh-pages branch:**
   ```bash
   git checkout --orphan gh-pages
   git rm -rf .
   git add index.html
   git commit -m "Initial GitHub Pages deployment"
   git push origin gh-pages
   ```

2. **Repository Settings:**
   - Go to Settings → Pages
   - Select branch: `gh-pages`
   - Folder: `/ (root)`

3. **Access at:** `https://amitnahum18.github.io/Data_Analyst_Agent/`

## 📂 Project Structure

```
Data_Analyst_Agent/
├── README.md                 # This file
├── .gitignore                # Git exclusions
├── .env.example              # Environment template
├── requirements.txt          # Python dependencies
├── SQL_query.py              # DuckDB query API (8001)
├── Update_DB.py              # CSV upload API (8000)
├── index.html                # Chat UI (or /docs/index.html)
├── workflow_SQL.json         # n8n SQL execution workflow
├── Rafi_Agent.json           # n8n AI agent workflow
└── my_database.duckdb        # DuckDB database (auto-created)
```

## 🔧 Configuration

### Environment Variables

Create `.env` file:
```env
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
N8N_WEBHOOK_URL=http://localhost:5678/webhook/xxxx-xxxx-xxxx
```

### DuckDB Connection

Edit `SQL_query.py` and `Update_DB.py` to change `DB_FILE`:
```python
DB_FILE = "my_database.duckdb"  # Change path if needed
```

### n8n Webhook Configuration

In Rafi Agent workflow:
1. Click "Chat Trigger" node
2. Copy webhook URL
3. Update `N8N_WEBHOOK_URL` in `.env`
4. Update `index.html` fetch URL to match

## 🚦 API Reference

### SQL Query API (Port 8001)

**POST** `/query/`

Request:
```json
{
  "query": "SELECT * FROM users LIMIT 10;"
}
```

Response:
```json
{
  "columns": ["id", "name", "email"],
  "data": [...]
}
```

### CSV Upload API (Port 8000)

**POST** `/upload-csv/`

- Multipart form data
- File parameter: `file`

Response:
```json
{
  "status": "success",
  "rows_inserted": 1000,
  "columns": [
    {"column_name": "id", "data_type": "BIGINT"},
    {"column_name": "name", "data_type": "VARCHAR"}
  ]
}
```

## 🤖 RAFI Agent Capabilities

- **Schema Awareness**: Auto-detects table structure
- **Multi-Step Analysis**: Chains multiple SQL queries
- **Best Practices**: Uses parameterized queries, proper escaping
- **Error Handling**: Graceful degradation and retry logic
- **Hebrew Output**: Responses formatted in Hebrew with markdown tables

## 📝 Usage Examples

### Example 1: CSV Upload
1. Click "Upload CSV" in chat
2. Select your data file
3. RAFI processes and loads data into DuckDB

### Example 2: Query Analysis
- User: "Who has the highest salary?"
- RAFI: Runs `SELECT * FROM users ORDER BY salary DESC LIMIT 1;`
- Returns result with Hebrew explanation

### Example 3: Multi-Step Analysis
- User: "What's the average by department?"
- RAFI: Fetches schema → Runs aggregation query → Formats table

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "users table not found" | Upload CSV via chat interface first |
| CORS errors | Check n8n webhook URL configuration |
| DuckDB locked | Ensure only one connection at a time |
| API timeout | Check FastAPI servers are running on ports 8000/8001 |
| Missing columns | Re-upload CSV to update schema |

## 📚 Documentation

- [n8n Docs](https://docs.n8n.io/)
- [DuckDB Guide](https://duckdb.org/docs/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/)
- [OpenRouter API](https://openrouter.ai/)

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**Amit Nahum** - AI Data Analyst Project
- GitHub: [@amitnahum18](https://github.com/amitnahum18)

## 🤝 Contributing

Contributions welcome! Please fork, create a feature branch, and submit a pull request.

---

**Last Updated**: 2026-03-23 22:48:42