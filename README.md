# ⚡ AI Prompt Engineering Lab
### Tata Steel · AI Initiative · Powered by Groq

A professional, interactive Streamlit application for learning and practising prompt engineering through realistic corporate business scenarios.

---

## 🚀 Quick Start (Local)

### Step 1 — Install Python
Make sure you have **Python 3.9+** installed.
```bash
python --version
```

### Step 2 — Clone / Download this project
```bash
# If using git
git clone <your-repo-url>
cd prompt_lab

# Or just unzip the downloaded folder and cd into it
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Get your FREE Groq API Key
1. Go to 👉 **[console.groq.com](https://console.groq.com)**
2. Sign up (free — no credit card needed)
3. Click **"API Keys"** in the left sidebar
4. Click **"Create API Key"** → give it a name → copy the key (starts with `gsk_...`)
5. Paste it into the app's sidebar when you run it

### Step 5 — Run the app
```bash
streamlit run app.py
```
The app opens at **http://localhost:8501**

---

## ☁️ Deploy to Streamlit Cloud (Free Sharing)

1. Push this project to a **GitHub repository**
2. Go to **[share.streamlit.io](https://share.streamlit.io)**
3. Sign in with GitHub
4. Click **"New app"** → Select your repo → Set `app.py` as the main file
5. Click **"Deploy"** — done! You'll get a public URL to share

**Important:** Don't commit your API key to GitHub. Users enter their own key in the app sidebar.

---

## 📁 Project Structure

```
prompt_lab/
├── app.py              # Main Streamlit application
├── cases.py            # All 5 business case definitions
├── utils.py            # Prompt scoring & evaluation logic
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🏢 The 5 Business Cases

| # | Case | Department | Difficulty |
|---|------|-----------|-----------|
| 1 | 🎓 Learning & Development | HR · L&D | Medium |
| 2 | 👥 Recruitment & Talent Acquisition | HR · Talent | High |
| 3 | 🛒 Procurement & Vendor Selection | Finance | Medium |
| 4 | 🖥️ IT Helpdesk Support | IT | Low |
| 5 | 📅 Leave Management & Workforce Planning | HR · Ops | High |

---

## 🤖 Models Available (Groq — all free tier)

| Model | Speed | Best For |
|-------|-------|----------|
| `llama-3.3-70b-versatile` | Fast | Best quality (default) |
| `llama-3.1-8b-instant` | Very fast | Quick testing |
| `mixtral-8x7b-32768` | Fast | Long context |
| `gemma2-9b-it` | Fast | Concise outputs |

---

## ✨ Features

- **5 real corporate scenarios** (L&D, Recruitment, Procurement, IT, Leave)
- **Full case brief** with business context, objectives, inputs, expected outputs
- **Starter prompt templates** for each case
- **Real AI responses** via Groq API (free, fast)
- **Automatic prompt scoring** (0–100) across 5 criteria
- **Detailed feedback** with actionable improvement tips
- **Prompt checklist** — see exactly what's missing
- **Session history** with export to JSON
- **Dark theme** professional UI

---

## 🔑 Groq API — Free Tier Limits

- **6,000 tokens/minute** (plenty for normal use)
- **500,000 tokens/day** on free tier
- No credit card required

---

## 📬 Questions?
Built for Tata Steel AI Internship Project. Contact your project supervisor for access queries.
