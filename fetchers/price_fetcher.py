"""
وحدة سحب بيانات الأسعار التاريخية.

⚠️ ملاحظة مهمة:
تغطية أسهم بورصة الكويت في مصادر البيانات المجانية (مثل yfinance) محدودة
أو غير موجودة لبعض الرموز. هذا الملف مبني بحيث تقدر تبدّل مصدر البيانات
بسهولة (دالة واحدة فقط) بدون ما تغيّر باقي البوت.

إذا ما اشتغل yfinance مع رموزك، بدائل تقدر تبحث عنها:
- investing.com (عبر مكتبات غير رسمية)
- Wall Street / Mubasher (بيانات السوق الخليجي)
- مزود بيانات مدفوع يغطي بورصة الكويت مباشرة
"""

import pandas as pd

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False


def fetch_price_history(ticker: str, days: int = 365) -> pd.DataFrame:
    """
    يسحب بيانات OHLCV (فتح/أعلى/أدنى/إغلاق/حجم) اليومية لسهم معين.

    يرجع DataFrame بالأعمدة: Open, High, Low, Close, Volume
    أو DataFrame فاضي إذا فشل السحب (بدل ما يكسر البرنامج).
    """
    if not YFINANCE_AVAILABLE:
        print("⚠️ مكتبة yfinance غير مثبتة. شغّل: pip install yfinance")
        return pd.DataFrame()

    try:
        data = yf.download(
            ticker,
            period=f"{days}d",
            interval="1d",
            progress=False,
        )
        if data.empty:
            print(f"⚠️ ما رجعت بيانات لسهم {ticker} — تأكد من صحة الرمز أو جرّب مصدر ثاني.")
        return data
    except Exception as e:
        print(f"⚠️ خطأ في سحب بيانات {ticker}: {e}")
        return pd.DataFrame()


def resample_weekly(daily_df: pd.DataFrame) -> pd.DataFrame:
    """يحوّل بيانات يومية إلى أسبوعية — مناسب لأسلوب التداول الأسبوعي-الشهري."""
    if daily_df.empty:
        return daily_df

    weekly = daily_df.resample("W").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum",
    })
    return weekly.dropna()
