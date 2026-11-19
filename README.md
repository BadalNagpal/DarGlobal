# DarGlobal & Wasalt Real Estate AI Chatbot

An AI-powered luxury & regional real estate conversational application that scrapes and aggregates live property data from **DarGlobal** (`darglobal.co.uk`) and **Wasalt** (`wasalt.com`).

---

## 🌟 Live Working URL
- **Public URL**: [https://arrangement-acer-earning-mills.trycloudflare.com](https://arrangement-acer-earning-mills.trycloudflare.com)
- **Local URL**: `http://localhost:8000`

---

## 🚀 Features
1. **Multi-Source Web Scraping**:
   - **DarGlobal**: Scraped 42 luxury developments across Dubai, Oman, Spain, Qatar, and Saudi Arabia (including high-profile collaborations with Trump Organization, Pagani, Automobili Lamborghini, Missoni, Aston Martin, and Fendi Casa).
   - **Wasalt**: Scraped 128 active property listings across Riyadh and Jeddah (villas, residential floors, apartments for rent and sale with prices, bedrooms, areas, and districts).
2. **Hybrid Dual-Engine Chatbot**:
   - **OpenRouter Free Models**: Connects to free models on OpenRouter (e.g. `meta-llama/llama-3.3-70b-instruct:free`, `google/gemini-2.0-flash-exp:free`, `deepseek/deepseek-r1:free`).
   - **Built-in RAG Knowledge Advisor**: Built-in retrieval-augmented generation engine that provides direct, grounded real estate recommendations even without an API key.
3. **Interactive UI**:
   - Modern luxury dark-mode interface with Tailwind CSS and FontAwesome.
   - Live real estate knowledge feed showing matching properties dynamically alongside chat.
   - Pre-configured quick prompt chips for instant exploration.
   - In-app modal to add or switch OpenRouter keys and models at any time.

---

## 🐳 Docker Containerization

### Run with Docker:
```bash
docker build -t darglobal-wasalt-chatbot .
docker run -p 8000:8000 darglobal-wasalt-chatbot
```

### Run with Docker Compose:
```bash
docker compose up -d
```

---

## 💻 Local Development Setup

1. **Create virtual environment**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Start the application**:
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
4. Access the app in your browser at `http://localhost:8000`.
