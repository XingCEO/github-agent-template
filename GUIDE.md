# 📚 GitHub Actions AI Agent 完整教學指南

> 不需要買硬體、不需要開著電腦，用 GitHub 免費算力讓 AI 替你工作

**適合對象**：想要自動化日常任務的創業者、內容創作者、研究員，不需要寫過程式也能照著做。

---

## 目錄

1. [為什麼 GitHub Actions 是最省錢的 AI Agent 平台](#1-為什麼-github-actions-是最省錢的-ai-agent-平台)
2. [GitHub Actions 基礎概念](#2-github-actions-基礎概念)
3. [設定你的第一個 AI 定時任務](#3-設定你的第一個-ai-定時任務)
4. [Anthropic API 申請和使用](#4-anthropic-api-申請和使用)
5. [Telegram 整合](#5-telegram-整合)
6. [進階：多 Workflow 協作與條件觸發](#6-進階多-workflow-協作與條件觸發)
7. [成本計算](#7-成本計算)
8. [常見錯誤和解法](#8-常見錯誤和解法)

---

## 1. 為什麼 GitHub Actions 是最省錢的 AI Agent 平台

### 問題背景

很多人想讓 AI 幫自己做重複性工作——每天早上整理新聞、每週追蹤競品、定時發送報告。但這些任務需要一台「永遠開著的電腦」來執行。

常見的解法和問題：

**本機電腦**：電腦要一直開著，出門就停了，電費也是成本。

**購買 VPS（虛擬主機）**：每月 $5-20 美金，還要學 Linux、設定 cron、管 Python 環境，對非工程師太麻煩。

**Zapier / Make**：操作直覺，但一旦需要自訂 AI 邏輯，很快就超出免費額度，每月要付 $20-50 美金。

**GitHub Actions 的優勢**：

GitHub 本來是讓工程師做程式碼測試的工具，但它的「執行任意程式碼」特性讓它成為絕佳的 AI Agent 平台：

- 🆓 **真的免費**：私有 repo 每月 2000 分鐘，個人用完全夠
- 🌐 **全雲端**：在 GitHub 的伺服器上跑，跟你的電腦完全無關
- 🔐 **安全存 API Key**：GitHub Secrets 功能讓 API Key 不會外洩
- 📅 **原生支援 cron**：比 Windows 工作排程器或 Mac launchd 設定更簡單
- 🔄 **觸發方式多元**：定時、手動、程式碼更新、外部 webhook 都支援

### 和付費課程的差別

市面上有付費課程在教「GitHub Actions AI Agent」，收費 $200-500 美金。這個開源版本提供同樣的核心架構，**完全免費**。差別在於付費課程有影片說明和社群，但如果你願意讀文字教學，這份指南涵蓋了你需要的一切。

---

## 2. GitHub Actions 基礎概念

GitHub Actions 乍看複雜，但核心只有幾個概念。

### Workflow（工作流程）

一個 Workflow 就是「一件自動化的事情」。例如：「每天早上 8 點執行早報腳本」就是一個 workflow。

Workflow 用 YAML 檔案定義，存放在 `.github/workflows/` 目錄下。

### Trigger（觸發條件）

告訴 GitHub「什麼時候執行這個 Workflow」。

常用觸發條件：

```yaml
on:
  # 定時執行（cron 語法）
  schedule:
    - cron: '0 23 * * *'   # 每天 UTC 23:00（台灣時間 07:00）
  
  # 手動觸發（在 Actions 頁面按按鈕）
  workflow_dispatch:
  
  # 程式碼 push 時觸發
  push:
    branches: [main]
  
  # 外部 webhook 觸發（進階用法）
  repository_dispatch:
    types: [custom-event]
```

### Job（任務）

一個 Workflow 可以有多個 Job，每個 Job 跑在獨立的虛擬機器上。Job 預設並行執行，也可以設定依賴關係讓它們依序執行。

### Step（步驟）

一個 Job 由多個 Step 組成，依序執行。每個 Step 可以是：
- 直接執行 shell 命令（`run: echo "hello"`）
- 使用現成的 Action（`uses: actions/checkout@v4`）

### 一個完整的 Workflow 例子

```yaml
name: My First AI Task           # Workflow 名稱（顯示在 Actions 頁面）

on:
  schedule:
    - cron: '0 23 * * *'        # 每天 UTC 23:00 執行
  workflow_dispatch:              # 也允許手動觸發

jobs:
  run-ai-task:                    # Job 名稱（自己取）
    runs-on: ubuntu-latest        # 用 Ubuntu 虛擬機

    steps:
      - name: 取得程式碼
        uses: actions/checkout@v4  # 把 repo 的檔案下載到虛擬機

      - name: 安裝 Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: 安裝套件
        run: pip install anthropic requests

      - name: 執行 AI 腳本
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}  # 從 Secrets 讀取
        run: python scripts/my_script.py
```

### 理解 `${{ secrets.XXX }}`

這個語法是讀取你在 GitHub 設定的 Secrets。你不會在 yml 檔案裡直接寫 API Key（那樣不安全），而是：
1. 在 GitHub repo 的 Settings → Secrets 設定 `ANTHROPIC_API_KEY`
2. 在 workflow 裡用 `${{ secrets.ANTHROPIC_API_KEY }}` 引用它

這樣 API Key 不會出現在任何 log 或程式碼裡，非常安全。

---

## 3. 設定你的第一個 AI 定時任務

### 前置需求

在開始前，你需要：
- 一個 GitHub 帳號（免費）
- 一個 Anthropic API Key
- 一個 Telegram Bot

### Step 1：Fork 模板

1. 前往這個 repo 的頁面
2. 點擊右上角 **Fork**
3. 選擇你的帳號
4. 建議改為 **Private**（Settings → 最底部 → Change visibility）

### Step 2：設定 Secrets

1. 進入你的 repo
2. 點 **Settings** → **Secrets and variables** → **Actions**
3. 點 **New repository secret**
4. 名稱：`ANTHROPIC_API_KEY`，值：你的 API Key
5. 重複以上步驟設定 `TELEGRAM_BOT_TOKEN` 和 `TELEGRAM_CHAT_ID`

### Step 3：手動測試

1. 點 **Actions** 頁籤
2. 左側選 **Daily AI Brief**
3. 右側點 **Run workflow** → **Run workflow**
4. 等約 1-2 分鐘
5. 點進去看執行 log
6. 去 Telegram 確認收到訊息

### Step 4：確認自動執行

設定完成後，Workflow 會按照 cron 時間自動執行。你可以在 Actions 頁面看到每次執行的歷史記錄。

---

## 4. Anthropic API 申請和使用

### 申請步驟

1. 前往 [console.anthropic.com](https://console.anthropic.com)
2. 點 **Sign Up** 用 Email 或 Google 帳號註冊
3. 需要綁定信用卡（用於用量計費）
4. 新帳號通常有 $5 免費額度
5. 前往 **API Keys** → **Create Key**
6. 命名（例如：`github-actions-agent`）
7. 複製 Key 妥善保存（只顯示一次）

### 模型選擇和省錢技巧

Anthropic 提供多種模型，**強烈建議先用 Haiku**：

| 模型 | 輸入費用/百萬 token | 輸出費用/百萬 token | 適合用途 |
|------|-------------------|-------------------|---------|
| Claude Haiku 3.5 | $0.80 | $4.00 | **日常自動任務（推薦）** |
| Claude Sonnet 4 | $3.00 | $15.00 | 複雜分析、需要高品質時 |
| Claude Opus 4 | $15.00 | $75.00 | 最高品質，非必要別用 |

**省 Token 技巧**：

**1. 系統提示詞盡量短**
不要把整個任務說明都放在 system prompt。只放角色設定（1-3 句話）。

**2. 限制輸出長度**
設定合理的 `max_tokens`：
- 每日摘要：600-800 tokens 夠了
- 分析報告：1000-1500 tokens
- 不要設 4096 然後讓 Claude 自由發揮

**3. 明確指定格式**
「請用 5 個條列式重點回答，每點不超過 20 字」比「請詳細分析」省 5 倍 token。

**4. 先用 Haiku 測試**
開發時用 Haiku，確認邏輯正確後再考慮要不要換 Sonnet。

**5. 批次請求而不是多次請求**
把 5 個問題合成一個 prompt，比發 5 次請求省 80% 的成本（因為每次請求都有最小 token 消耗）。

### 監控用量

在 [console.anthropic.com/settings/billing](https://console.anthropic.com/settings/billing) 可以設定用量上限，防止超支。建議設定每月 $5 上限。

---

## 5. Telegram 整合

### 為什麼用 Telegram？

- **完全免費**，沒有 API 費用
- Bot API 簡單，一個 HTTP 請求就能發訊息
- 支援 Markdown 格式，表格、粗體、連結都能用
- 可以發到個人、群組、頻道
- 訊息推送即時，不像 Email 可能進垃圾郵件

### 建立 Bot 的完整步驟

**1. 找到 BotFather**

在 Telegram 搜尋 `@BotFather`（官方帳號，有藍色勾勾），點進去。

**2. 建立新 Bot**

發送：
```
/newbot
```

按照提示：
- 輸入 Bot 的顯示名稱（例如：`我的每日情報`）
- 輸入 Bot 的用戶名（必須以 `bot` 結尾，例如：`my_daily_intel_bot`）

成功後 BotFather 會給你一段 Token，格式像：
```
5823456789:AAHdqTcvCH1vGWJxfSeofShs0K5PALDsaw
```
這就是 `TELEGRAM_BOT_TOKEN`。

**3. 啟動 Bot**

在 Telegram 搜尋你剛建立的 Bot 名稱，點進去，發送 `/start`。**這步很重要**——Bot 必須先被你啟動，才能發訊息給你。

**4. 取得 Chat ID**

在瀏覽器開啟：
```
https://api.telegram.org/bot{你的TOKEN}/getUpdates
```

（把 `{你的TOKEN}` 換成實際 Token）

在回傳的 JSON 中找 `"chat":{"id":` 後面的數字。例如：
```json
"chat": {
  "id": 123456789,
  "first_name": "你的名字",
  "type": "private"
}
```
`123456789` 就是你的 `TELEGRAM_CHAT_ID`。

**5. 傳送訊息格式**

這個模板使用 Markdown 格式，支援：
- `*粗體*` → **粗體**
- `_斜體_` → *斜體*
- `` `等寬字體` `` → `等寬字體`
- `[連結文字](URL)` → 超連結

---

## 6. 進階：多 Workflow 協作與條件觸發

### 多個 Workflow 協作

當你有多個 Workflow 時，可以設計讓它們互相呼叫：

```yaml
# workflow A 完成後觸發 workflow B
- name: Trigger next workflow
  run: |
    curl -X POST \
      -H "Authorization: token ${{ secrets.GITHUB_TOKEN }}" \
      -H "Accept: application/vnd.github.v3+json" \
      https://api.github.com/repos/${{ github.repository }}/dispatches \
      -d '{"event_type":"analysis-complete"}'
```

另一個 Workflow 監聽這個事件：

```yaml
on:
  repository_dispatch:
    types: [analysis-complete]
```

### 條件觸發（只在特定情況執行步驟）

```yaml
steps:
  - name: 執行腳本
    id: run-script
    run: python scripts/check_condition.py
    
  - name: 只在條件成立時執行
    if: steps.run-script.outputs.should_notify == 'true'
    run: python scripts/send_notification.py
```

在 Python 腳本中輸出條件：
```python
import os

# 設定 GitHub Actions output
def set_output(name, value):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write(f"{name}={value}\n")

# 決定是否需要通知
if something_important_happened:
    set_output("should_notify", "true")
else:
    set_output("should_notify", "false")
```

### 儲存執行結果

把每次執行的結果寫回 repo，建立歷史記錄：

```yaml
- name: Save result to repo
  run: |
    mkdir -p results
    echo "${{ steps.analysis.outputs.result }}" > results/$(date +%Y-%m-%d).md
    git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
    git config user.name "GitHub Actions"
    git add results/
    git commit -m "Auto: add result $(date +%Y-%m-%d)" || echo "No changes"
    git push
```

### 使用 Matrix 並行執行多個任務

```yaml
jobs:
  research:
    strategy:
      matrix:
        keyword: ["AI automation", "no-code tools", "SaaS pricing"]
    steps:
      - run: python scripts/research.py "${{ matrix.keyword }}"
```

這樣三個關鍵字會同時並行搜尋，速度是循序執行的 3 倍。

### 使用快取加速執行

每次安裝 pip 套件要花 30-60 秒，用快取可以跳過這步：

```yaml
- name: Cache pip dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

- name: Install dependencies
  run: pip install -r requirements.txt
```

### 把結果輸出到 GitHub Summary

讓執行結果直接顯示在 Actions 頁面，不用進 log 找：

```python
import os

summary = "## 今日分析結果\n\n- 發現 3 個市場機會\n- 競品無重大動態"

with open(os.environ['GITHUB_STEP_SUMMARY'], 'w') as f:
    f.write(summary)
```

---

## 7. 成本計算

### GitHub Actions 免費額度

| Repo 類型 | 免費額度/月 | 超出費用 |
|---------|-----------|---------|
| 公開 repo | **無限制** | 免費 |
| 私有 repo | 2,000 分鐘 | $0.008/分鐘 |

**這個模板的實際用量**：

| Workflow | 執行時間 | 每月執行次數 | 每月用量 |
|---------|---------|------------|--------|
| 每日早報 | ~2 分鐘 | 30 次 | 60 分鐘 |
| 每日市場研究 | ~3 分鐘 | 30 次 | 90 分鐘 |
| 每週競品監控 | ~4 分鐘 | 4 次 | 16 分鐘 |
| **合計** | | | **~166 分鐘** |

2000 分鐘的免費額度，我們只用了 **8%**。還剩 1834 分鐘可以跑其他任務。

### Claude API 費用估算

使用 Claude Haiku 3.5（最便宜，效果已經很好）：

| 任務 | 每次 input token | 每次 output token | 每次費用 |
|-----|----------------|-------------------|---------|
| 每日早報 | ~500 | ~800 | $0.00072 |
| 市場研究（3關鍵字） | ~2000 | ~1800 | $0.0088 |
| 競品監控（3競品） | ~3000 | ~1500 | $0.0084 |

**每月 API 費用**：
- 早報：$0.00072 × 30 = $0.022
- 市場研究：$0.0088 × 30 = $0.264
- 競品監控：$0.0084 × 4 = $0.034

**月費合計：約 $0.32 USD（約台幣 10 元）**

### Brave Search 免費額度

免費方案每月 2000 次查詢。

我們的用量：市場研究 3 關鍵字 × 3 次搜尋 × 30 天 = 270 次，競品監控 3 競品 × 3 次搜尋 × 4 週 = 36 次。

**合計 306 次，遠低於 2000 次上限。**

### 總結

| 服務 | 月費（台幣） |
|-----|------------|
| GitHub Actions | NT$0 |
| Claude Haiku API | NT$10 |
| Brave Search | NT$0 |
| Telegram | NT$0 |
| **合計** | **約 NT$10** |

---

## 8. 常見錯誤和解法

### 🔴 錯誤：`Error: Resource not accessible by integration`

**原因**：Workflow 試圖寫回 repo，但沒有權限。

**解法**：在 Settings → Actions → General → Workflow permissions 勾選 **Read and write permissions**。

---

### 🔴 錯誤：`AuthenticationError: 401`（Anthropic）

**原因**：API Key 不正確或已過期。

**解法**：
1. 去 [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys) 確認 Key 是否有效
2. 在 GitHub Secrets 重新設定 `ANTHROPIC_API_KEY`
3. 確認 Secret 名稱拼寫正確（大小寫敏感）

---

### 🔴 錯誤：Telegram 沒收到訊息

**原因通常是**：
1. Bot 沒被啟動（需要先跟 Bot 發訊息）
2. Chat ID 錯誤
3. Bot Token 錯誤

**排查步驟**：
1. 直接在瀏覽器測試：`https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=test`
2. 如果瀏覽器有回傳 `{"ok":true,...}`，設定正確
3. 如果沒有，看錯誤訊息，通常是 Token 或 Chat ID 的問題

---

### 🔴 錯誤：Workflow 不執行

**可能原因**：

1. **新 fork 的 repo Actions 被禁用**  
   解法：到 Settings → Actions → General，選 Allow all actions

2. **cron 時間有誤**  
   解法：用 [crontab.guru](https://crontab.guru) 驗證 cron 語法

3. **GitHub cron 延遲**  
   GitHub 的 cron 任務在高峰時可能延遲 15-30 分鐘，這是正常現象

4. **repo 超過 60 天沒有活動**  
   GitHub 會自動停用 schedule trigger。解法：進 Actions 頁面手動 enable

---

### 🔴 錯誤：Python 腳本執行失敗

**排查步驟**：

1. 在 Actions log 找紅色的錯誤訊息
2. 常見錯誤：
   - `ModuleNotFoundError`：pip install 沒裝到需要的套件
   - `KeyError`：環境變數名稱拼錯
   - `requests.exceptions.Timeout`：網路請求超時，通常重跑一次就好

3. 本地測試：複製 Secrets 的值設成本地環境變數，在本機跑腳本測試

---

### 🟡 警告：免費額度快用完了怎麼辦

**GitHub Actions 分鐘**：
- 把非必要的 workflow 改為每週執行而不是每天
- 把多個任務合並到同一個 workflow
- 考慮把 repo 改為公開（免費無限分鐘，但程式碼公開）

**Anthropic API Token**：
- 換用更便宜的模型（Haiku 3.5）
- 縮短提示詞
- 降低 max_tokens 設定
- 設定每月用量上限防止超支

---

## 延伸學習

掌握了基礎後，可以進一步探索：

- **GitHub Actions 官方文件**：[docs.github.com/en/actions](https://docs.github.com/en/actions)
- **Anthropic API 文件**：[docs.anthropic.com](https://docs.anthropic.com)
- **crontab 時間計算**：[crontab.guru](https://crontab.guru)
- **Brave Search API 文件**：[api.search.brave.com/app/documentation](https://api.search.brave.com/app/documentation/web-search/get-started)

---

## 總結

GitHub Actions AI Agent 的核心邏輯非常簡單：

```
cron 觸發 → 虛擬機啟動 → 跑 Python 腳本 → 呼叫 AI API → 發送結果到 Telegram → 虛擬機關閉
```

你不需要伺服器、不需要懂 DevOps、不需要花錢買工具。只要會複製貼上 API Key，這套系統就能替你每天工作。

**下一步**：看 [SETUP.md](SETUP.md) 設定你的第一個 workflow！

---

*本指南持續更新。發現問題或有建議請開 Issue。*
