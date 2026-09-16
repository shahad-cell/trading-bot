"""
نقطة التشغيل الرئيسية للبوت التحليلي.

يسوي:
1. يجيب قائمة الأسهم الحلال المسموحة (ويستبعد الذهب تلقائياً).
2. يسحب بيانات كل سهم.
3. يحوّلها أسبوعية (مناسبة لأسلوب سوينق/بوزيشن).
4. يحسب المؤشرات الفنية.
5. يطبع بطاقة قرار لكل سهم.

شغّله بـ: python main.py
"""

from data.halal_watchlist import HALAL_STOCKS
from config import EXCLUDED_ASSETS
from fetchers.price_fetcher import fetch_price_history, resample_weekly
from analysis.technical import compute_indicators
from signals.signal_generator import generate_signal_card, print_signal_card


def is_excluded(ticker: str) -> bool:
    return any(excluded in ticker.upper() for excluded in EXCLUDED_ASSETS)


def run():
    print("🔍 جاري تحليل قائمة الأسهم الحلال...\n")

    for stock in HALAL_STOCKS:
        ticker = stock["ticker"]
        name = stock["name"]

        if is_excluded(ticker):
            continue  # حماية إضافية حتى لو دخل بالخطأ

        daily_data = fetch_price_history(ticker)
        if daily_data.empty:
            print(f"⚠️ تخطي {name} ({ticker}) — لا توجد بيانات.\n")
            continue

        weekly_data = resample_weekly(daily_data)
        indicators = compute_indicators(weekly_data)
        card = generate_signal_card(ticker, name, indicators)
        print_signal_card(card)
        print()

    print("✅ انتهى التحليل. هذي معلومات للمراجعة فقط — القرار والتنفيذ إلك.")


if __name__ == "__main__":
    run()
