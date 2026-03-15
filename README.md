# 🤖 GitHub Actions AI Agent Template

**用 GitHub 免費算力跑 AI 自動化任務，不需要買硬體、不需要開著電腦**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 繁體中文說明

### 這是什麼？

這是一個可以直接 Fork 的 GitHub 模板倉庫，讓你用 **GitHub Actions 的免費算力** 跑 AI 自動化任務。

無論是每天早上自動發一份 AI 生成的市場情報到 Telegram，還是每週自動追蹤競品動態，全都在雲端自動運行。**你只需要 Fork 這個 Repo，設定幾個 API Key，就完成了。**

### 為什麼用 GitHub Actions？

| 方案 | 費用 | 需要電腦開著？ | 設定難度 |
|------|------|--------------|---------|
| **GitHub Actions** | **免費（2000分鐘/月）** | **不需要** | ⭐⭐ |
| 本機電腦 + cron | 電費 | 需要 | ⭐ |
| VPS 雲端主機 | $5-20/月 | 不需要 | ⭐⭐⭐ |
| Zapier/Make | $20+/月 | 不需要 | ⭐⭐ |
| AWS Lambda | 使用量計費 | 不需要 | ⭐⭐⭐⭐ |

**結論**：GitHub Actions 是個人和小團隊跑 AI 定時任務的最佳選擇——完全免費、無需維護、夠穩定。

### 功能列表

| Workflow | 執行時間 | 功能 |
|----------|---------|------|
| 🌅 每日 AI 早報 | 台灣時間 07:50 | Claude 生成早報 → Telegram |
| 📊 每日市場研究 | 台灣時間 09:00 | Brave 搜尋 + Claude 分析 → Telegram |
| 🕵️ 每週競品監控 | 週一 10:00 | 搜尋競品動態 + 威脅評估 → Telegram |

### 快速開始（3 步驟）

```
1️⃣  Fork 這個 Repo（右上角 Fork 按鈕）

2️⃣  在 Settings → Secrets 設定 API Keys：
    - ANTHROPIC_API_KEY
    - TELEGRAM_BOT_TOKEN
    - TELEGRAM_CHAT_ID

3️⃣  前往 Actions → Daily AI Brief → Run workflow 手動測試
```

詳細設定步驟請看 👉 [SETUP.md](SETUP.md)

完整教學指南請看 👉 [GUIDE.md](GUIDE.md)

### 費用估算

> **每月總費用 < NT$5（幾乎免費）**

- GitHub Actions：**免費**（私有 repo 每月 2000 分鐘）
- Claude Haiku 3.5 API：每月約 **$0.10-0.50 USD**（視使用量）
- Brave Search API：**免費**（每月 2000 次查詢）
- Telegram：**完全免費**

### 所需 API Keys

| 服務 | 用途 | 免費額度 | 申請連結 |
|------|------|---------|---------|
| Anthropic | AI 生成 | 有（需信用卡驗證） | [console.anthropic.com](https://console.anthropic.com) |
| Telegram Bot | 接收通知 | 永久免費 | [t.me/BotFather](https://t.me/BotFather) |
| Brave Search | 搜尋網路 | 2000次/月免費 | [brave.com/search/api](https://brave.com/search/api/) |

---

## English Description

### What is this?

A ready-to-fork GitHub template that runs AI automation tasks using **GitHub Actions' free compute**. No hardware needed, no server required, no subscription fees.

Fork → Set API keys → Done. Your AI agents run automatically in the cloud.

### Why GitHub Actions?

- ✅ **2,000 free minutes/month** (private repos) or unlimited (public repos)
- ✅ **No server to maintain** — GitHub handles everything
- ✅ **Schedule or webhook triggers** — run on cron or on-demand
- ✅ **Secure secrets storage** — API keys stored safely
- ✅ **Free for most personal use cases**

### Quick Start (3 Steps)

1. **Fork** this repo (click the Fork button above)
2. **Set secrets** in Settings → Secrets → Actions:
   - `ANTHROPIC_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
3. **Test** it: Actions → Daily AI Brief → Run workflow

See [SETUP.md](SETUP.md) for detailed instructions and [GUIDE.md](GUIDE.md) for the full tutorial.

### Included Workflows

| Workflow | Schedule (Taiwan Time) | Description |
|----------|----------------------|-------------|
| Daily AI Brief | 07:50 daily | AI-generated morning brief → Telegram |
| Market Research | 09:00 daily | Web search + Claude analysis → Telegram |
| Competitor Monitor | Monday 10:00 | Weekly competitor tracking → Telegram |

---

## 授權 License

MIT — 隨意使用、修改、分享。

---

## 相關資源

- 📖 [完整教學 GUIDE.md](GUIDE.md)
- ⚙️ [設定指南 SETUP.md](SETUP.md)
- 🐛 發現問題？[開 Issue](../../issues)
- 💡 有想法？[開 Discussion](../../discussions)
