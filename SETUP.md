# ⚙️ 設定指南

從零開始到第一個 AI 自動任務，大約需要 15 分鐘。

---

## 步驟一：Fork 這個 Repo

1. 點擊右上角 **Fork** 按鈕
2. 選擇你的 GitHub 帳號
3. Fork 完成後，你有了自己的副本，可以任意修改

> ⚠️ **私有倉庫建議**：如果你要存放 API Key 之類的敏感設定，建議在 Fork 後把 repo 改為 **Private**（Settings → 最底部 Danger Zone → Change visibility）

---

## 步驟二：取得所需 API Keys

### 🤖 Anthropic API Key（必填）

1. 前往 [console.anthropic.com](https://console.anthropic.com)
2. 註冊帳號（需要信用卡，但新帳號有免費額度）
3. 點擊 **API Keys** → **Create Key**
4. 複製保存（只會顯示一次）

**費用參考**：
- Claude Haiku 3.5：輸入 $0.8/百萬 token，輸出 $4/百萬 token
- 每日早報約消耗 1000 token，每月成本 < $0.15

### 📱 Telegram Bot（必填）

#### 建立 Bot
1. 在 Telegram 搜尋 `@BotFather`
2. 發送 `/newbot`
3. 輸入 Bot 名稱（例如：MyDailyBriefBot）
4. 輸入 Bot 用戶名（必須以 `bot` 結尾，例如：`my_daily_brief_bot`）
5. BotFather 會給你一個 Token，格式：`1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ`

#### 取得 Chat ID
1. 先啟動你的 Bot（搜尋 Bot 名稱，點擊 Start）
2. 發送任意訊息給 Bot
3. 在瀏覽器開啟：`https://api.telegram.org/bot{你的TOKEN}/getUpdates`
4. 找到 `"chat":{"id":` 後面的數字，那就是你的 Chat ID
5. 也可以搜尋 `@userinfobot`，它會直接告訴你的 ID

#### 加入群組（可選）
如果要發送到群組：
1. 把 Bot 加入群組（管理員身份）
2. 在群組發送一則訊息
3. 用上述方法取得群組的 Chat ID（通常是負數，例如：`-1001234567890`）

### 🔍 Brave Search API Key（市場研究和競品監控需要）

1. 前往 [brave.com/search/api](https://brave.com/search/api/)
2. 點擊 **Get Started for Free**
3. 免費方案：每月 2000 次查詢，足夠個人使用
4. 建立 API Key 後複製

---

## 步驟三：設定 GitHub Secrets

1. 進入你 Fork 的 repo
2. 點擊 **Settings**（頂部導航）
3. 左側選單找 **Secrets and variables** → **Actions**
4. 點擊 **New repository secret** 新增以下設定：

| Secret 名稱 | 說明 | 必填 |
|-------------|------|------|
| `ANTHROPIC_API_KEY` | Anthropic API Key | ✅ |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | ✅ |
| `TELEGRAM_CHAT_ID` | Telegram Chat/Group ID | ✅ |
| `BRAVE_SEARCH_API_KEY` | Brave Search API Key | 市場研究需要 |
| `COMPETITOR_NAMES` | 競品名稱，逗號分隔 | 競品監控需要 |
| `CLAUDE_MODEL` | Claude 模型名（可選） | ❌ |
| `YOUR_PRODUCT` | 你的產品名（可選） | ❌ |

---

## 步驟四：手動測試

1. 前往你的 repo → **Actions** 頁籤
2. 左側選擇 **Daily AI Brief**
3. 點擊 **Run workflow** → **Run workflow**
4. 等待約 1-2 分鐘
5. 如果看到綠色勾勾 ✅，去 Telegram 看看收到了什麼！

如果出現紅色 ❌，點進去看 log 找錯誤訊息。

---

## 修改 Cron 時間

編輯 `.github/workflows/` 下的 yml 檔案，找到 `cron:` 那行：

```yaml
- cron: '50 23 * * *'
```

格式：`分 時 日 月 星期`（UTC 時間）

**常用時間換算（台灣 UTC+8）：**

| 台灣時間 | UTC cron 設定 |
|---------|--------------|
| 早上 07:00 | `0 23 * * *` |
| 早上 08:00 | `0 0 * * *` |
| 早上 09:00 | `0 1 * * *` |
| 下午 18:00 | `0 10 * * *` |
| 晚上 21:00 | `0 13 * * *` |

> 注意：GitHub cron 不保證精確到分鐘，可能有 ±15 分鐘誤差。

---

## 自訂早報主題

在 `.github/workflows/daily-brief.yml` 中取消以下行的注釋並修改：

```yaml
# BRIEF_TOPICS: "AI 新聞,科技產業,台灣商業"
```

改成：
```yaml
BRIEF_TOPICS: "你的主題1,你的主題2,你的主題3"
```

---

## 常見問題

### ❓ workflow 沒有執行

- 確認 repo 有 commit（新 fork 的 repo 有時需要先手動觸發一次）
- 檢查 cron 時間是否設定正確（UTC，不是台灣時間）
- Actions 可能需要在 Settings → Actions → General 中啟用

### ❓ 收不到 Telegram 訊息

1. 確認有先對 Bot 發過訊息（Bot 必須先被啟動）
2. 確認 Chat ID 正確（群組 ID 是負數）
3. 在 Actions log 中找 "Telegram" 相關錯誤

### ❓ Claude API 回傳錯誤

- `401 Unauthorized`：API Key 設定錯誤，重新確認
- `429 Too Many Requests`：請求過多，稍後再試或升級方案
- `500 Internal Server Error`：Anthropic 服務問題，等幾分鐘重試

### ❓ GitHub Actions 免費額度用完怎麼辦

- 免費：每月 2000 分鐘（私有 repo）/ 無限（公開 repo）
- 每次 workflow 大約用 2-3 分鐘
- 每日執行 3 個 workflow = 每月 ~270 分鐘，遠低於上限

### ❓ 如何停止某個 workflow

- 方法一：在 Actions → 選 workflow → 右上角 `...` → Disable workflow
- 方法二：刪除對應的 `.github/workflows/xxx.yml` 檔案

---

## 進階設定

### 條件執行（只在工作日執行）

```yaml
on:
  schedule:
    - cron: '50 23 * * 1-5'  # 週一到週五（UTC）
```

### 設定執行超時（避免 workflow 卡住）

```yaml
jobs:
  brief:
    runs-on: ubuntu-latest
    timeout-minutes: 10  # 超過 10 分鐘自動停止
```

### 儲存執行結果到 repo

可以用 GitHub Actions 把結果寫回 repo，當作歷史記錄：

```yaml
- name: Save result
  run: |
    echo "$RESULT" > results/$(date +%Y-%m-%d).txt
    git config user.email "action@github.com"
    git config user.name "GitHub Action"
    git add results/
    git commit -m "Add result $(date +%Y-%m-%d)" || true
    git push
```

---

有問題歡迎開 Issue！
