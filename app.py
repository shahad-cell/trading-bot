"""
لوحة العرض (Dashboard) — واجهة ويب بسيطة بدل الطرفية.
تشتغل بنفس محرك التحليل اللي بنيناه، بس بأزرار وبطاقات مرتبة.

تشغيل محلي: streamlit run app.py
"""

import streamlit as st
from data.halal_watchlist import HALAL_STOCKS
from config import EXCLUDED_ASSETS
from fetchers.price_fetcher import fetch_price_history, resample_weekly
from analysis.technical import compute_indicators
from signals.signal_generator import generate_signal_card

st.set_page_config(page_title="لوحة الأسهم الحلال", page_icon="📊", layout="wide")

# دعم بسيط للاتجاه من اليمين لليسار
st.markdown(
    """
    <style>
    html, body, [class*="css"] { direction: rtl; text-align: right; }
    </style>
    """,
    unsafe_allow_html=True,
)


def is_excluded(ticker: str) -> bool:
    return any(excluded in ticker.upper() for excluded in EXCLUDED_ASSETS)


@st.cache_data(ttl=3600)  # يخزن النتيجة ساعة كاملة، ما يسحب كل ضغطة زر
def analyze_ticker(ticker: str):
    daily = fetch_price_history(ticker)
    if daily.empty:
        return None
    weekly = resample_weekly(daily)
    return compute_indicators(weekly)


st.title("📊 لوحة الأسهم الحلال")
st.caption("معلومات تحليلية للمراجعة فقط — القرار والتنفيذ إلك دائماً.")

if st.button("🔍 حلل الأسهم الآن", type="primary"):
    with st.spinner("جاري تحليل الأسهم..."):
        for stock in HALAL_STOCKS:
            ticker, name = stock["ticker"], stock["name"]
            if is_excluded(ticker):
                continue

            indicators = analyze_ticker(ticker)

            with st.container(border=True):
                st.subheader(f"{name} ({ticker})")

                if not indicators or "error" in (indicators or {}):
                    st.warning("بيانات غير كافية لهذا السهم حالياً.")
                    continue

                card = generate_signal_card(ticker, name, indicators)

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("السعر الحالي", indicators["current_price"])
                col2.metric("RSI", indicators["rsi"])
                col3.metric("الدعم", indicators["support"])
                col4.metric("المقاومة", indicators["resistance"])

                st.write(f"**الاتجاه:** {indicators['trend']}")
                st.info(f"🔔 {card['attention_level']}")
else:
    st.info("اضغط الزر فوق عشان تبدأ التحليل.")

st.divider()
st.caption("⚠️ هذي أداة تحليل فقط، ليست توصية استثمارية أو فتوى شرعية.")
