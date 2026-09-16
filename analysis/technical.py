"""
وحدة التحليل الفني — مؤشرات مناسبة لأسلوب سوينق/بوزيشن (أسبوعي-شهري).
لا يعطي أوامر شراء/بيع، فقط يحسب القيم ويوصفها.
"""

import pandas as pd


def compute_indicators(df: pd.DataFrame) -> dict:
    """
    يحسب مجموعة مؤشرات فنية أساسية على بيانات أسعار (أسبوعية عادة).
    يرجع dict فيه القيم الحالية + وصف مبسط لكل واحد.
    """
    if df.empty or len(df) < 20:
        return {"error": "بيانات غير كافية للتحليل (نحتاج ٢٠ نقطة سعرية على الأقل)"}

    close = df["Close"]
    result = {}

    # --- المتوسطات المتحركة ---
    sma_10 = close.rolling(10).mean().iloc[-1]
    sma_20 = close.rolling(20).mean().iloc[-1]
    current_price = close.iloc[-1]

    result["current_price"] = round(float(current_price), 3)
    result["sma_10"] = round(float(sma_10), 3)
    result["sma_20"] = round(float(sma_20), 3)
    result["trend"] = (
        "اتجاه صاعد (السعر فوق المتوسطين)" if current_price > sma_10 > sma_20
        else "اتجاه هابط (السعر تحت المتوسطين)" if current_price < sma_10 < sma_20
        else "اتجاه غير واضح / تذبذب"
    )

    # --- RSI (مؤشر القوة النسبية) ---
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    current_rsi = round(float(rsi.iloc[-1]), 1)

    result["rsi"] = current_rsi
    result["rsi_note"] = (
        "منطقة تشبع شرائي (فوق ٧٠)" if current_rsi > 70
        else "منطقة تشبع بيعي (تحت ٣٠)" if current_rsi < 30
        else "منطقة محايدة"
    )

    # --- الدعم والمقاومة (تقريبي، بناءً على آخر ٢٠ نقطة) ---
    recent = df.tail(20)
    result["support"] = round(float(recent["Low"].min()), 3)
    result["resistance"] = round(float(recent["High"].max()), 3)

    return result
