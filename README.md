# Support AI RAG Agent (Knowledge Sync Service)

A lightweight, production-ready Python pipeline that scrapes customer support documentation, processes it into clean Markdown, synchronizes data incrementally using MD5 hashing, and feeds it into the Google Gemini Vector Store for RAG-based AI assistance.

## 🛠️ Setup & Local Execution

1. **Clone the repository** (Ensure the repository name does not contain any brand-specific keywords to maintain project anonymity).
2. **Configure your environment**:
   Copy `.env.sample` to `.env` and fill in your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key
Run the Daily Sync Job locally:

```bash
python main.py
```

Test the Assistant:
```bash
python bot_agent.py
```

🐋 Docker Implementation
The application is containerized to execute as a discrete daily scheduled task. The process runs once to synchronize data and terminates gracefully upon completion.

Build the Image
```bash
docker build -t knowledge-sync-agent .
```

Run the Container with Custom Name
Pass your API key as an environment variable and assign a specific container name to ensure secure and organized execution:

```bash
docker run --name my-sync-container --env-file .env knowledge-sync-agent
```
(The task executes main.py once, logs the delta sync metrics to Docker Desktop, and exits with status code 0).

🧠 Architecture Details
Chunking Strategy
Since the technical support documentation consists of short, highly structured articles (typically under 2,000 words), we utilize Gemini's Native Markdown Chunking via the client.files API. This preservation layer retains structural elements such as Markdown headers, lists, and deep-linked asset reference tables, optimizing context retrieval for the gemini-2.5-flash model.

Incremental Sync (Delta Updates)
To optimize platform resource usage and adhere to API rate limits, the pipeline implements an efficient delta tracking mechanism:

State Management: Tracks file modification states using cryptographic MD5 checksum hashes saved locally in sync_state.json.

Delta Analysis: Compares existing content states to dynamically classify changes into Added, Updated, or Skipped metrics.

Clean Sync: For any Updated status, the stale Cloud file is systematically purged before uploading the fresh version, preventing duplicate knowledge retrieval.

📊 Sample Execution Logs
Plaintext
==================================================
🚀 BẮT ĐẦU CHẠY TIẾN TRÌNH ĐỒNG BỘ TRI THỨC HÀNG NGÀY
==================================================
🔄 [Scraper] Đang cào dữ liệu từ OptiSigns...

📊 [Scraper Kết quả] Added: 0 | Updated: 0 | Skipped: 30

========== KẾT QUẢ JOB SỰ KIỆN ==========
📌 Tổng số bài viết THÊM MỚI (Added) : 0
📌 Tổng số bài viết CẬP NHẬT (Updated) : 0
📌 Tổng số bài viết BỎ QUA (Skipped)   : 30
=====================================
✅ Tiến trình kết thúc thành công. Exit Code: 0
