"""
قائمة الأسهم المسموح بتحليلها فقط (فلتر شرعي).

⚠️ مهم جداً:
هذه قائمة تجريبية (placeholder) بأمثلة فقط — لازم تستبدلها بقائمة رسمية
معتمدة من مصدر موثوق (بوبيان كابيتال، أو مؤشر بورصة الكويت الإسلامي،
أو مزود شرعي معروف). البوت لا يفتي بنفسه، هو فقط يلتزم بهالقائمة.

كل سهم = رمزه (Ticker) + اسمه + السوق.
"""

HALAL_STOCKS = [
    # مثال فقط — استبدل هذي بقائمتك الفعلية
    {"ticker": "BOUBYAN.KW", "name": "بنك بوبيان", "market": "Boursa Kuwait"},
    {"ticker": "KFH.KW", "name": "بيت التمويل الكويتي", "market": "Boursa Kuwait"},
    {"ticker": "AGLTY.KW", "name": "أجيليتي", "market": "Boursa Kuwait"},
]


def get_halal_tickers() -> list[str]:
    """يرجع قائمة الرموز فقط (بدون تفاصيل) لاستخدامها في الفلترة."""
    return [stock["ticker"] for stock in HALAL_STOCKS]


def is_halal(ticker: str) -> bool:
    """يتحقق إذا كان السهم موجود في القائمة الحلال."""
    return ticker.upper() in [t.upper() for t in get_halal_tickers()]
