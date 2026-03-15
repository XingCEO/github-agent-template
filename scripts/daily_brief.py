"""
daily_brief.py - 每日 AI 早報
GitHub Actions AI Agent Template

功能：
- 呼叫 Claude 生成今日重點早報
- 自動發送到 Telegram
- 每天台灣時間 07:50 自動執行

環境變數需求：
- ANTHROPIC_API_KEY
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID

選用環境變數：
- CLAUDE_MODEL（預設 claude-haiku-3-5，省 token）
- BRIEF_TOPICS（早報主題，逗號分隔）
"""

import os
import sys
import logging
from datetime import datetime, timezone, timedelta

# 加入 scripts 目錄到路徑（方便本地測試）
sys.path.insert(0, os.path.dirname(__file__))
from utils import call_claude, send_telegram, require_env, get_taiwan_time, get_today_date

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
#  設定
# ─────────────────────────────────────────────

DEFAULT_TOPICS = [
    "AI 與科技產業動態",
    "台灣與亞洲商業新聞",
    "全球總體經濟",
    "創業與新創生態",
]

SYSTEM_PROMPT = """你是一個專業的商業情報分析師，專門為忙碌的創業者提供每日簡報。
你的風格：
- 精準、有洞察，不廢話
- 用繁體中文
- 每個主題 3-5 個重點，條列式
- 最後附上「今日行動建議」1 條
- 使用 emoji 讓格式更清晰"""


def build_prompt(topics: list[str], date: str) -> str:
    topics_str = "\n".join(f"- {t}" for t in topics)
    return f"""今天是 {date}（台灣時間）。

請為我生成今日早報，涵蓋以下主題：
{topics_str}

格式要求：
1. 開頭：「🌅 {date} 早報」
2. 每個主題用 emoji + 標題開頭
3. 重點條列（每點一行，用 • 符號）
4. 結尾：「💡 今日行動建議」一條具體建議

注意：這是基於你的訓練知識生成的摘要，請誠實說明知識截止日期的限制。"""


def run():
    logger.info("=== Daily Brief started ===")

    # 1. 驗證環境變數
    try:
        require_env("ANTHROPIC_API_KEY", "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID")
    except EnvironmentError as e:
        logger.error(str(e))
        sys.exit(1)

    # 2. 讀取設定
    model = os.environ.get("CLAUDE_MODEL", "claude-haiku-3-5")
    topics_env = os.environ.get("BRIEF_TOPICS", "")
    topics = [t.strip() for t in topics_env.split(",") if t.strip()] or DEFAULT_TOPICS

    date_str = get_today_date()
    taiwan_time = get_taiwan_time()

    logger.info(f"Date: {date_str}, Model: {model}")
    logger.info(f"Topics: {topics}")

    # 3. 生成早報
    prompt = build_prompt(topics, date_str)

    try:
        brief_content = call_claude(
            prompt=prompt,
            system=SYSTEM_PROMPT,
            model=model,
            max_tokens=1500,
        )
    except Exception as e:
        logger.error(f"Claude API failed: {e}")
        # 失敗時發送錯誤通知
        send_telegram(f"⚠️ 早報生成失敗\n\n錯誤：{e}\n\n時間：{taiwan_time}")
        sys.exit(1)

    # 4. 組合訊息
    footer = f"\n\n─────────────────\n⏰ 生成時間：{taiwan_time}\n🤖 模型：{model}"
    full_message = brief_content + footer

    logger.info(f"Brief generated: {len(brief_content)} chars")

    # 5. 發送到 Telegram
    success = send_telegram(full_message)

    if success:
        logger.info("=== Daily Brief completed successfully ===")
    else:
        logger.error("Failed to send Telegram message")
        sys.exit(1)


if __name__ == "__main__":
    run()
