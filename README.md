# 🦞 GitHub Actions AI Agent Template

**繁體中文** | **[English](#english)**

> 用 GitHub 免費算力跑 AI 自動化任務，不需要買硬體、不需要開著電腦

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![GitHub Stars](https://img.shields.io/github/stars/XingCEO/github-agent-template?style=social)](https://github.com/XingCEO/github-agent-template)
[![GitHub Forks](https://img.shields.io/github/forks/XingCEO/github-agent-template?style=social)](https://github.com/XingCEO/github-agent-template)

> 作者：**[超星男孩 XingCEO](https://github.com/XingCEO)** | 繁體中文 AI 自動化模板，持續更新維護

---

## 目錄

- [這是什麼？](#這是什麼)
- [為什麼用 GitHub Actions？](#為什麼用-github-actions)
- [免費版 vs 完整版](#免費版-vs-完整版)
- [快速開始](#快速開始3-步驟)
- [Workflows 說明](#包含的-workflows)
- [所需 API Keys](#所需-api-keys)
- [費用估算](#費用估算)
- [授權聲明](#授權聲明)
- [English](#english)

---

## 這是什麼？

這是一個可以直接 **Fork** 的 GitHub 模板倉庫，讓你用 **GitHub Actions 的免費算力**跑 AI 自動化任務。

- 🌅 每天早上自動生成 AI 市場情報，發到你的 Telegram
- 📊 每日自動搜尋 AI 趨勢、數位產品機會，整理成報告
- 🕵️ 每週自動監控競品動態，讓你不錯過市場變化
- 🔔 全部在雲端運行，**你人在睡覺它也在工作**

**Fork → 設定 API Key → 完成。** 不需要架主機、不需要電腦開著、不需要懂後端。

---

## 為什麼用 GitHub Actions？

| 方案 | 月費 | 需要電腦開著？ | 設定難度 | 穩定度 |
|------|:----:|:------------:|:-------:|:------:|
| **GitHub Actions（本模板）** | **免費** | **❌ 不需要** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 本機電腦 + cron | 電費 | ✅ 需要 | ⭐ | ⭐⭐ |
| VPS 雲端主機 | $5–20 USD | ❌ 不需要 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Zapier / Make | $20+ USD | ❌ 不需要 | ⭐⭐ | ⭐⭐⭐⭐ |
| AWS Lambda | 使用量計費 | ❌ 不需要 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**結論**：GitHub Actions 每月 2,000 分鐘免費算力，跑這些 AI 任務每月大約只用 30–60 分鐘，永遠不會超額。

---

## 免費版 vs 完整版

| 功能 | 免費版（此 Repo） | 完整版 |
|------|:---:|:---:|
| 每日 AI 早報 | ✅ | ✅ |
| 每日市場研究 | ✅ | ✅ |
| 每週競品監控 | ✅ | ✅ |
| 繁體中文完整教學（17,000 字） | ✅ | ✅ |
| LINE 通知整合 | ❌ | ✅ |
| 電商賣家自動化（蝦皮/商品描述） | ❌ | ✅ |
| 社群貼文自動排程腳本 | ❌ | ✅ |
| 財務報表 AI 分析 | ❌ | ✅ |
| 進階 prompt 優化（省 70% token） | ❌ | ✅ |
| 客製化 workflow 模板 x5 | ❌ | ✅ |
| 作者一對一設定支援 | ❌ | ✅ |
| 新模板優先取得 + 更新通知 | ❌ | ✅ |

> **👉 [取得完整版](https://github.com/XingCEO)** — 8 個進階模板 + 設定支援

---

## 快速開始（3 步驟）

### Step 1：Fork 這個 Repo

點右上角 **Fork** 按鈕，Fork 到你自己的帳號。

### Step 2：設定 Secrets

進入你 Fork 後的 Repo → **Settings → Secrets and variables → Actions → New repository secret**，新增以下三個：

| Secret 名稱 | 說明 | 取得方式 |
|------------|------|---------|
| `ANTHROPIC_API_KEY` | Claude AI 的 API Key | [console.anthropic.com](https://console.anthropic.com) |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | 找 [@BotFather](https://t.me/BotFather) 建立 Bot |
| `TELEGRAM_CHAT_ID` | 你的 Telegram 用戶 ID | 找 [@userinfobot](https://t.me/userinfobot) 查詢 |

### Step 3：手動測試

進入 **Actions → Daily AI Brief → Run workflow**，點綠色按鈕手動觸發一次，確認 Telegram 有收到訊息。

---

📖 **詳細設定步驟（含截圖說明）→ [SETUP.md](SETUP.md)**
📚 **完整教學（8 章節，17,000 字）→ [GUIDE.md](GUIDE.md)**

---

## 包含的 Workflows

### 🌅 每日 AI 早報（`daily-brief.yml`）
- **觸發時間**：台灣時間每天 07:50
- **功能**：搜尋最新 AI 新聞、台灣科技動態、數位產品趨勢，由 Claude 整理成早報，發送到 Telegram
- **支援手動觸發**：任何時候都可以在 Actions 頁面手動跑

### 📊 每日市場研究（`market-research.yml`）
- **觸發時間**：台灣時間每天 09:00
- **功能**：用 Brave Search 搜尋 AI agent 趨勢、數位產品機會、競爭對手動態，Claude 分析後發報告
- **輸出**：結構化 Markdown 報告 → Telegram

### 🕵️ 每週競品監控（`competitor-monitor.yml`）
- **觸發時間**：台灣時間每週一 10:00
- **功能**：追蹤指定競品的最新動態、定價變化、用戶反饋，生成威脅評估報告
- **可自訂**：修改 `scripts/competitor_monitor.py` 裡的競品清單

---

## 所需 API Keys

| 服務 | 用途 | 免費額度 |
|------|------|---------|
| **Anthropic Claude** | AI 生成內容 | 需信用卡驗證，有免費額度 |
| **Telegram Bot** | 接收通知 | 永久完全免費 |
| **Brave Search API** | 搜尋即時資訊 | 每月 2,000 次免費 |

---

## 費用估算

```
GitHub Actions     : 免費（每月 2,000 分鐘，本模板約用 30-60 分鐘）
Brave Search API   : 免費（每月 2,000 次查詢）
Telegram Bot       : 免費
Claude Haiku API   : 約 $0.10–$0.50 USD / 月（視使用量）

每月總費用 ≈ NT$3–15
```

---

## 授權聲明

本專案採用 **[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)** 授權：

- ✅ 可以免費使用、Fork、修改、分享
- ✅ 修改後必須標註原作者（超星男孩 XingCEO）
- ❌ **不得用於商業販售或商業服務**
- ❌ 不得移除作者署名和授權聲明

商業授權洽詢：[github.com/XingCEO](https://github.com/XingCEO)

---

---

## English

**[繁體中文](#)** | **English**

> Run AI automation tasks using GitHub's free compute — no hardware, no server, no monthly fees.

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

### What is this?

A fork-ready GitHub template that runs **AI automation workflows** using GitHub Actions' free compute.

- 🌅 Daily AI morning brief → Telegram (every day at 07:50 Taiwan time)
- 📊 Daily market research → Telegram (web search + Claude analysis)
- 🕵️ Weekly competitor monitoring → Telegram (threat assessment report)

**Everything runs in the cloud automatically. Fork → Set API keys → Done.**

### Why GitHub Actions?

| Option | Monthly Cost | Always-on Machine? | Setup |
|--------|:-----------:|:-----------------:|:-----:|
| **GitHub Actions (this template)** | **Free** | **Not needed** | Easy |
| Local computer + cron | Electricity | Required | Easy |
| VPS / Cloud server | $5–20 USD | Not needed | Hard |
| Zapier / Make | $20+ USD | Not needed | Medium |

GitHub Actions gives you **2,000 free minutes/month**. These workflows use ~30–60 minutes/month — you'll never hit the limit.

### Quick Start (3 Steps)

**Step 1: Fork this repo** (click Fork button above)

**Step 2: Add Secrets** in your fork → Settings → Secrets → Actions:

| Secret | Description | Where to get |
|--------|-------------|-------------|
| `ANTHROPIC_API_KEY` | Claude AI API key | [console.anthropic.com](https://console.anthropic.com) |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | Create via [@BotFather](https://t.me/BotFather) |
| `TELEGRAM_CHAT_ID` | Your Telegram user ID | Check via [@userinfobot](https://t.me/userinfobot) |

**Step 3: Test it** → Actions → Daily AI Brief → Run workflow → Check Telegram

📖 Full setup guide → [SETUP.md](SETUP.md)
📚 Complete tutorial (8 chapters) → [GUIDE.md](GUIDE.md)

### Free vs Pro

| Feature | Free (this repo) | Pro Version |
|---------|:---:|:---:|
| Daily AI brief | ✅ | ✅ |
| Market research | ✅ | ✅ |
| Competitor monitoring | ✅ | ✅ |
| Full Chinese tutorial (17,000 words) | ✅ | ✅ |
| LINE notification integration | ❌ | ✅ |
| E-commerce automation scripts | ❌ | ✅ |
| Social media scheduling | ❌ | ✅ |
| Advanced prompt optimization (save 70% tokens) | ❌ | ✅ |
| 5 custom workflow templates | ❌ | ✅ |
| 1-on-1 setup support | ❌ | ✅ |

> **👉 [Get Pro Version](https://github.com/XingCEO)** — 8 advanced templates + setup support

### Cost Estimate

```
GitHub Actions   : Free (2,000 min/month; this uses ~30-60 min)
Brave Search     : Free (2,000 queries/month)
Telegram         : Free
Claude Haiku API : ~$0.10–$0.50 USD/month

Total: < $1 USD/month
```

### License

**CC BY-NC-SA 4.0** — Free to use, fork, and adapt. **Commercial use prohibited.** Attribution required.

For commercial licensing: [github.com/XingCEO](https://github.com/XingCEO)

---

⭐ **If this helped you, please give it a star — it helps others find this project.**
