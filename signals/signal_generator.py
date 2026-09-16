"""
وحدة توليد "بطاقة القرار" — تجمع التحليل الفني (ولاحقاً الإخباري)
في شكل منظم يعرض المعطيات والأسباب، بدون ما يصدر أمر تنفيذ.
"""


def generate_signal_card(ticker: str, name: str, indicators: dict) -> dict:
    """
    يبني بطاقة قرار واحدة لسهم معين.
    هذي البطاقة "معلومات للمراجعة" — القرار النهائي دايم إلك.
    """
    if "error" in indicators:
        return {
            "ticker": ticker,
            "name": name,
            "status": "بيانات غير كافية",
            "reasoning": [indicators["error"]],
        }

    reasoning = []
    reasoning.append(f"السعر الحالي: {indicators['current_price']}")
    reasoning.append(f"الاتجاه: {indicators['trend']}")
    reasoning.append(f"RSI: {indicators['rsi']} — {indicators['rsi_note']}")
    reasoning.append(
        f"نطاق التداول الأخير: دعم {indicators['support']} / مقاومة {indicators['resistance']}"
    )

    # ملاحظة: هذا "مستوى انتباه" وصفي فقط، مو توصية.
    # المعايير هنا تقديرية وتقدر تعدلها حسب أسلوبك.
    if indicators["rsi"] < 30 and "صاعد" not in indicators["trend"]:
        attention = "منطقة تستاهل مراجعة أعمق (تشبع بيعي + اتجاه غير صاعد)"
    elif indicators["rsi"] > 70:
        attention = "منطقة تشبع شرائي — احتمال ارتداد أو استمرار، يحتاج سياق إضافي"
    else:
        attention = "لا يوجد مستوى تنبيه واضح حالياً"

    return {
        "ticker": ticker,
        "name": name,
        "status": "تم التحليل",
        "attention_level": attention,
        "reasoning": reasoning,
    }


def print_signal_card(card: dict) -> None:
    """يطبع بطاقة القرار بشكل مقروء في الطرفية."""
    print("=" * 50)
    print(f"📊 {card['name']} ({card['ticker']})")
    print("-" * 50)
    if card["status"] != "تم التحليل":
        print(f"⚠️ {card['status']}")
        for line in card.get("reasoning", []):
            print(f"  - {line}")
        return

    for line in card["reasoning"]:
        print(f"  • {line}")
    print(f"\n  🔔 {card['attention_level']}")
