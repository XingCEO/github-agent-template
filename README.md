# 🦞 GitHub Actions AI Agent Template

**用 GitHub 免費算力跑 AI 自動化任務，不需要買硬體、不需要開著電腦**

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![GitHub Stars](https://img.shields.io/github/stars/XingCEO/github-agent-template?style=social)](https://github.com/XingCEO/github-agent-template)

> **作者：[超星男孩 XingCEO](https://github.com/XingCEO)**
> 繁體中文 AI 自動化模板，持續更新維護。

---

## 這是什麼？

這是一個可以直接 Fork 的 GitHub 模板倉庫，讓你用 **GitHub Actions 的免費算力** 跑 AI 自動化任務。

無論是每天早上自動發一份 AI 生成的市場情報到 Telegram，還是每週自動追蹤競品動態，全都在雲端自動運行。**你只需要 Fork 這個 Repo，設定幾個 API Key，就完成了。**

---

## 免費版 vs 完整版

| 功能 | 免費版（此 Repo） | 完整版（付費）|
|------|:---:|:---:|
| 每日 AI 早報 | ✅ | ✅ |
| 每日市場研究 | ✅ | ✅ |
| 每週競品監控 | ✅ | ✅ |
| 繁體中文完整教學（17,000 字） | ✅ | ✅ |
| 電商賣家自動化模板 | ❌ | ✅ |
| LINE 通知整合 | ❌ | ✅ |
| 社群貼文自動排程腳本 | ❌ | ✅ |
| 財務報表 AI 分析 | ❌ | ✅ |
| 進階 prompt 優化（省 70% token）| ❌ | ✅ |
| 作者一對一設定支援 | ❌ | ✅ |
| 更新通知 + 新模板優先取得 | ❌ | ✅ |

**👉 [取得完整版](https://github.com/XingCEO) — 包含 8 個進階模板 + 設定支援**

---

## 為什麼用 GitHub Actions？

| 方案 | 月費 | 需要電腦開著？ | 設定難度 |
|------|------|--------------|---------|
| **GitHub Actions（本模板）** | **免費** | **不需要** | ⭐⭐ |
| 本機電腦 + cron | 電費 | 需要 | ⭐ |
| VPS 雲端主機 | $5-20 USD | 不需要 | ⭐⭐⭐ |
| Zapier/Make | $20+ USD | 不需要 | ⭐⭐ |

**月費估算：Claude API ~$0.10-0.50 USD，其餘免費。每月不到 NT$20。**

---

## 快速開始（3 步驟）

```
1️⃣  Fork 這個 Repo（右上角 Fork 按鈕）

2️⃣  在 Settings → Secrets → Actions 設定：
    - ANTHROPIC_API_KEY   (從 console.anthropic.com 取得)
    - TELEGRAM_BOT_TOKEN  (從 @BotFather 取得)
    - TELEGRAM_CHAT_ID    (你的 Telegram 用戶 ID)

3️⃣  Actions → Daily AI Brief → Run workflow 手動測試
```

📖 詳細步驟 → [SETUP.md](SETUP.md)
📚 完整教學 → [GUIDE.md](GUIDE.md)

---

## 包含的 Workflows

| Workflow | 執行時間（台灣） | 功能 |
|----------|----------------|------|
| 🌅 Daily AI Brief | 每天 07:50 | Claude 生成早報 → Telegram |
| 📊 Market Research | 每天 09:00 | Brave 搜尋 + Claude 分析 → Telegram |
| 🕵️ Competitor Monitor | 週一 10:00 | 競品追蹤 + 威脅評估 → Telegram |

---

## English Summary

A fork-ready GitHub template for running AI automation with GitHub Actions' free compute. No hardware, no server, no monthly fees.

**Workflows included:** Daily AI brief, market research, competitor monitoring — all delivered to Telegram.

**Cost:** ~$0.10-0.50/month (Claude API only). Everything else is free.

See [SETUP.md](SETUP.md) and [GUIDE.md](GUIDE.md) for full instructions.

---

## 授權聲明

本專案採用 **CC BY-NC-SA 4.0** 授權：
- ✅ 可以免費使用、修改、分享
- ✅ 需標註原作者（超星男孩 XingCEO）
- ❌ **不得用於商業販售**
- ❌ 不得移除作者署名

商業授權洽詢：[github.com/XingCEO](https://github.com/XingCEO)

---

## 相關連結

- 📖 [完整教學 GUIDE.md](GUIDE.md)
- ⚙️ [設定指南 SETUP.md](SETUP.md)
- 🐛 [回報問題](../../issues)
- ⭐ 覺得有用請給 Star，讓更多人找到這個專案
