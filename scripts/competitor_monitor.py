"""
competitor_monitor.py - 每週競品監控腳本
GitHub Actions AI Agent Template

功能：
- 搜尋競品最新動態（新功能、定價、行銷策略等）
- Claude 分析威脅程度和機會
- 生成週報發送到 Telegram

環境變數需求：
- ANTHROPIC_API_KEY
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID
- BRAVE_SEARCH_API_KEY
- COMPETITOR_NAMES（競品名稱，逗號分隔）

選用：
- CLAUDE_MODEL（預設 claude-haiku-3-5）
- YOUR_PRODUCT（你的產品名稱，用於比較分析）
"""

import os
import sys
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


SYSTEM_PROMPT = """你是一個競爭情報分析師，專門追蹤競品動態並提供策略建議。
分析風格：
- 繁體中文
- 客觀評估，不誇大威脅
- 重點放在「對我們有什麼影響」
- 具體的應對建議"""


def monitor_competitor(name: str, model: str, your_product: str = "") -> dict:
    """監控單一競品"""
    logger.info(f"Monitoring competitor: {name}")

    # 搜尋競品最新動態
    queries = [
        f"{name} new feature update 2025",
        f"{name} pricing change",
        f"{name} review complaint",
    ]

    all_results = []
    for query in queries:
        results = brave_search(query=query, count=3)
        all_results.extend(results)

    if not all_results:
        return {"name": name, "analysis": "（本週無重大動態）", "threat_level": "低"}

    formatted = format_search_results(all_results[:9])  # 最多 9 筆

    product_context = f"（我們的產品：{your_product}）" if your_product else ""

    prompt = f"""分析競品「{name}」本週動態{product_context}：

搜尋結果：
{formatted}

請提供：
1. 🆕 本週主要動態（條列，最多3點）
2. 💪 競品新優勢
3. 😤 用戶抱怨/弱點（從評論中找）
4. 🎯 威脅等級：低/中/高（一個詞）
5. 💡 我們的應對建議（1條）"""

    try:
        analysis = call_claude(
            prompt=prompt,
            system=SYSTEM_PROMPT,
            model=model,
            max_tokens=500,
        )

        # 嘗試從分析中提取威脅等級
        threat = "中"
        if "威脅等級：低" in analysis or "低" in analysis[:200]:
            threat = "低"
        elif "威脅等級：高" in analysis or "高" in analysis[:200]:
            threat = "高"

        return {"name": name, "analysis": analysis, "threat_level": threat}
    except Exception as e:
        logger.error(f"Analysis failed for {name}: {e}")
        return {"name": name, "analysis": f"（分析失敗：{e}）", "threat_level": "未知"}


def build_report(analyses: list[dict], date: str, taiwan_time: str) -> str:
    """組合競品週報"""
    threat_emoji = {"低": "🟢", "中": "🟡", "高": "🔴", "未知": "⚪"}

    header = f"🕵️ *競品週報 {date}*\n\n"
    sections = []

    for item in analyses:
        emoji = threat_emoji.get(item["threat_level"], "⚪")
        section = (
            f"━━━━━━━━━━━━━━━\n"
            f"{emoji} *{item['name']}*（威脅：{item['threat_level']}）\n\n"
            f"{item['analysis']}"
        )
        sections.append(section)

    # 摘要
    high_threats = [a["name"] for a in analyses if a["threat_level"] == "高"]
    summary = ""
    if high_threats:
        summary = f"\n\n🚨 *高威脅競品*：{', '.join(high_threats)}\n需要優先關注！"

    footer = f"\n\n━━━━━━━━━━━━━━━\n⏰ 報告時間：{taiwan_time}"

    return header + "\n\n".join(sections) + summary + footer


def run():
    logger.info("=== Competitor Monitor started ===")

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
    competitors_env = os.environ.get("COMPETITOR_NAMES", "")
    your_product = os.environ.get("YOUR_PRODUCT", "")

    competitors = [c.strip() for c in competitors_env.split(",") if c.strip()]
    if not competitors:
        logger.error("COMPETITOR_NAMES is not set. Please add it to GitHub Secrets.")
        send_telegram("⚠️ 競品監控設定缺失\n\n請在 GitHub Secrets 中設定 COMPETITOR_NAMES（逗號分隔的競品名稱）")
        sys.exit(1)

    date_str = get_today_date()
    taiwan_time = get_taiwan_time()

    logger.info(f"Monitoring {len(competitors)} competitors: {competitors}")

    # 3. 監控每個競品
    analyses = []
    for competitor in competitors:
        result = monitor_competitor(competitor, model, your_product)
        analyses.append(result)

    # 4. 組合報告
    report = build_report(analyses, date_str, taiwan_time)

    logger.info(f"Report generated: {len(report)} chars")

    # 5. 發送到 Telegram
    success = send_telegram(report)

    if success:
        logger.info("=== Competitor Monitor completed successfully ===")
    else:
        logger.error("Failed to send report")
        sys.exit(1)


if __name__ == "__main__":
    run()
