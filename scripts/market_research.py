"""
market_research.py - 每日市場研究腳本
GitHub Actions AI Agent Template

功能：
- 用 Brave Search 搜尋指定關鍵字
- 將搜尋結果送給 Claude 分析
- 生成結構化市場情報報告
- 發送到 Telegram

環境變數需求：
- ANTHROPIC_API_KEY
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID
- BRAVE_SEARCH_API_KEY

選用環境變數：
- RESEARCH_KEYWORDS（搜尋關鍵字，逗號分隔）
- CLAUDE_MODEL（預設 claude-haiku-3-5）
"""

import os
import sys
import json
import logging

sys.path.insert(0, os.path.dirname(__file__))
from utils import (
    call_claude,
    send_telegram,
    brave_search,
    format_search_results,
    require_env,
    get_taiwan_time,
    get_today_date,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
#  設定
# ─────────────────────────────────────────────

DEFAULT_KEYWORDS = [
    "AI agent automation 2025",
    "no-code AI tools market",
    "GitHub Actions use cases",
]

SYSTEM_PROMPT = """你是一個市場研究分析師，專門分析 AI 與科技產業趨勢。
風格要求：
- 繁體中文
- 從搜尋結果中提取關鍵洞察
- 識別市場機會和風險
- 具體、可行動的結論
- 使用條列式格式"""


def analyze_keyword(keyword: str, model: str) -> dict:
    """搜尋並分析單一關鍵字"""
    logger.info(f"Researching: {keyword}")

    # 搜尋
    results = brave_search(query=keyword, count=5)
    if not results:
        return {"keyword": keyword, "analysis": "（搜尋無結果）", "results_count": 0}

    # 格式化搜尋結果
    formatted = format_search_results(results)

    # 請 Claude 分析
    prompt = f"""根據以下搜尋結果，分析關鍵字「{keyword}」的市場情況：

{formatted}

請提供：
1. 🔍 核心發現（2-3點）
2. 📈 市場趨勢
3. 💰 商業機會
4. ⚠️ 需注意的風險
5. 🎯 建議行動（1條具體建議）"""

    try:
        analysis = call_claude(
            prompt=prompt,
            system=SYSTEM_PROMPT,
            model=model,
            max_tokens=600,
        )
        return {
            "keyword": keyword,
            "analysis": analysis,
            "results_count": len(results),
        }
    except Exception as e:
        logger.error(f"Analysis failed for '{keyword}': {e}")
        return {"keyword": keyword, "analysis": f"（分析失敗：{e}）", "results_count": len(results)}


def build_report(analyses: list[dict], date: str, taiwan_time: str) -> str:
    """組合完整報告"""
    header = f"📊 *{date} 市場研究報告*\n\n"
    sections = []

    for item in analyses:
        kw = item["keyword"]
        analysis = item["analysis"]
        count = item["results_count"]
        section = f"━━━━━━━━━━━━━━━\n🔎 *{kw}*（找到 {count} 筆結果）\n\n{analysis}"
        sections.append(section)

    footer = f"\n\n━━━━━━━━━━━━━━━\n⏰ 報告時間：{taiwan_time}"

    return header + "\n\n".join(sections) + footer


def run():
    logger.info("=== Market Research started ===")

    # 1. 驗證環境變數
    try:
        require_env(
            "ANTHROPIC_API_KEY",
            "TELEGRAM_BOT_TOKEN",
            "TELEGRAM_CHAT_ID",
            "BRAVE_SEARCH_API_KEY",
        )
    except EnvironmentError as e:
        logger.error(str(e))
        sys.exit(1)

    # 2. 讀取設定
    model = os.environ.get("CLAUDE_MODEL", "claude-haiku-3-5")
    keywords_env = os.environ.get("RESEARCH_KEYWORDS", "")
    keywords = [k.strip() for k in keywords_env.split(",") if k.strip()] or DEFAULT_KEYWORDS

    date_str = get_today_date()
    taiwan_time = get_taiwan_time()

    logger.info(f"Keywords to research: {keywords}")

    # 3. 研究每個關鍵字
    analyses = []
    for keyword in keywords:
        result = analyze_keyword(keyword, model)
        analyses.append(result)

    # 4. 組合報告
    report = build_report(analyses, date_str, taiwan_time)

    logger.info(f"Report generated: {len(report)} chars")

    # 5. 發送到 Telegram
    success = send_telegram(report)

    if success:
        logger.info("=== Market Research completed successfully ===")
    else:
        logger.error("Failed to send report")
        sys.exit(1)


if __name__ == "__main__":
    run()
