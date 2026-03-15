"""
utils.py - 共用工具模組
GitHub Actions AI Agent Template
"""

import os
import json
import time
import logging
import requests
from typing import Optional, Any

# 設定 logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
#  Telegram
# ─────────────────────────────────────────────

def send_telegram(
    message: str,
    bot_token: Optional[str] = None,
    chat_id: Optional[str] = None,
    parse_mode: str = "Markdown",
    disable_preview: bool = True,
    max_retries: int = 3,
) -> bool:
    """
    發送訊息到 Telegram。

    Args:
        message: 要發送的訊息（支援 Markdown）
        bot_token: Bot Token（優先使用，否則從環境變數讀取）
        chat_id: Chat ID（優先使用，否則從環境變數讀取）
        parse_mode: 解析模式，"Markdown" 或 "HTML"
        disable_preview: 是否停用連結預覽
        max_retries: 失敗重試次數

    Returns:
        bool: 發送成功回傳 True
    """
    token = bot_token or os.environ.get("TELEGRAM_BOT_TOKEN")
    cid = chat_id or os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not cid:
        logger.error("Telegram credentials missing: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    # Telegram 單則訊息上限 4096 字元，超過需要分割
    chunks = _split_message(message, max_len=4000)

    for i, chunk in enumerate(chunks):
        payload = {
            "chat_id": cid,
            "text": chunk,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_preview,
        }

        for attempt in range(1, max_retries + 1):
            try:
                resp = requests.post(url, json=payload, timeout=15)
                resp.raise_for_status()
                data = resp.json()
                if data.get("ok"):
                    logger.info(f"Telegram message {i+1}/{len(chunks)} sent successfully")
                    break
                else:
                    logger.warning(f"Telegram API error: {data}")
            except requests.RequestException as e:
                logger.warning(f"Telegram attempt {attempt}/{max_retries} failed: {e}")
                if attempt < max_retries:
                    time.sleep(2 ** attempt)  # exponential backoff
                else:
                    logger.error("All Telegram retries exhausted")
                    return False

        # 避免 flood 限制
        if i < len(chunks) - 1:
            time.sleep(0.5)

    return True


def _split_message(text: str, max_len: int = 4000) -> list[str]:
    """將長訊息分割成多個段落"""
    if len(text) <= max_len:
        return [text]

    chunks = []
    while text:
        if len(text) <= max_len:
            chunks.append(text)
            break
        # 嘗試在換行處切割
        split_at = text.rfind("\n", 0, max_len)
        if split_at == -1:
            split_at = max_len
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip("\n")
    return chunks


# ─────────────────────────────────────────────
#  Anthropic / Claude
# ─────────────────────────────────────────────

def call_claude(
    prompt: str,
    system: str = "You are a helpful assistant.",
    model: str = "claude-haiku-3-5",
    max_tokens: int = 1024,
    api_key: Optional[str] = None,
) -> str:
    """
    呼叫 Anthropic Claude API。

    Args:
        prompt: 使用者訊息
        system: 系統提示詞
        model: 模型名稱（建議用 haiku 省錢）
        max_tokens: 最大輸出 token 數
        api_key: API Key（優先使用，否則從環境變數讀取）

    Returns:
        str: Claude 的回覆文字
    """
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("anthropic package not installed. Run: pip install anthropic")

    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise ValueError("ANTHROPIC_API_KEY not set")

    client = anthropic.Anthropic(api_key=key)

    logger.info(f"Calling Claude ({model}), max_tokens={max_tokens}")
    start = time.time()

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )

    elapsed = time.time() - start
    usage = message.usage
    logger.info(
        f"Claude response: {elapsed:.1f}s, "
        f"input_tokens={usage.input_tokens}, output_tokens={usage.output_tokens}"
    )

    return message.content[0].text


# ─────────────────────────────────────────────
#  Brave Search
# ─────────────────────────────────────────────

def brave_search(
    query: str,
    count: int = 5,
    api_key: Optional[str] = None,
) -> list[dict]:
    """
    使用 Brave Search API 搜尋網路。

    Args:
        query: 搜尋關鍵字
        count: 結果數量（最多 20）
        api_key: Brave API Key（優先使用，否則從環境變數讀取）

    Returns:
        list[dict]: 搜尋結果列表，每項包含 title/url/description
    """
    key = api_key or os.environ.get("BRAVE_SEARCH_API_KEY")
    if not key:
        raise ValueError("BRAVE_SEARCH_API_KEY not set")

    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": key,
    }
    params = {"q": query, "count": min(count, 20)}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        results = []
        for item in data.get("web", {}).get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "description": item.get("description", ""),
            })
        logger.info(f"Brave search '{query}': {len(results)} results")
        return results

    except requests.RequestException as e:
        logger.error(f"Brave search failed: {e}")
        return []


def format_search_results(results: list[dict]) -> str:
    """將搜尋結果格式化成文字供 Claude 分析"""
    if not results:
        return "（無搜尋結果）"

    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"{i}. **{r['title']}**")
        lines.append(f"   URL: {r['url']}")
        lines.append(f"   {r['description']}")
        lines.append("")
    return "\n".join(lines)


# ─────────────────────────────────────────────
#  環境變數驗證
# ─────────────────────────────────────────────

def require_env(*keys: str) -> dict[str, str]:
    """
    確認必要環境變數存在，缺少則拋出例外。

    Usage:
        env = require_env("ANTHROPIC_API_KEY", "TELEGRAM_BOT_TOKEN")
    """
    missing = [k for k in keys if not os.environ.get(k)]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Please set them in GitHub Secrets (Settings → Secrets and variables → Actions)"
        )
    return {k: os.environ[k] for k in keys}


# ─────────────────────────────────────────────
#  日期工具
# ─────────────────────────────────────────────

def get_taiwan_time() -> str:
    """取得台灣時間字串（不依賴 pytz，用 UTC+8 計算）"""
    from datetime import datetime, timezone, timedelta
    tz_tw = timezone(timedelta(hours=8))
    now = datetime.now(tz=tz_tw)
    return now.strftime("%Y-%m-%d %H:%M")


def get_today_date() -> str:
    """取得今日日期（台灣時間，YYYY-MM-DD）"""
    from datetime import datetime, timezone, timedelta
    tz_tw = timezone(timedelta(hours=8))
    return datetime.now(tz=tz_tw).strftime("%Y-%m-%d")
