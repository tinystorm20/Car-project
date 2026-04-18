import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="Car Project Strategy Center v2.0", layout="wide")

st.title("🚀 Car Project 전략 관제 대시보드 v2.0")
st.markdown("---")

# [1] 데이터 및 설정 관리
# 미국의 평균 영업일(주말/공휴일 제외)은 연간 약 252일입니다. 
# 이를 12개월로 나누면 월 평균 약 21일입니다.
AVG_TRADING_DAYS = 21 

st.sidebar.header("⚙️ 기본 투자 설정")
daily_budget = st.sidebar.number_input("일일 총 투자금 (원)", value=29500, step=500)
# 업데이트 1: 월 평균 투자액 재계산 (영업일 기준)
monthly_investment = daily_budget * AVG_TRADING_DAYS 

target_dividend = st.sidebar.number_input("목표 월 분배금 (원)", value=650000)
avg_yield = st.sidebar.slider("전체 포트폴리오 예상 월 수익률 (%)", 0.0, 5.0, 3.0, 0.1) / 100

# [2] 종목별 비중 및 최근 분배금 트렌드 데이터 (가상 데이터 포함)
# 실제 데이터 기반 트렌드 분석 섹션
st.subheader("📈 종목별 분배금 트렌드 및 전략 제안")

# 분석을 위한 가상 히스토리 데이터 (질문자님의 엑셀 데이터를 기반으로 분석 로직 구성)
trend_data = {
    "NVDY": [0.82, 0.85, 0.84], # 최근 3개월 주당 분배금
    "PLTY": [0.40, 0.42, 0.45],
    "MSTY": [1.20, 1.45, 1.50],
    "TSLY": [0.20, 0.18, 0.16],
    "QDTE": [0.30, 0.33, 0.35],
}

col_t1, col_t2 = st.columns([2, 1])

with col_t1:
    # 트렌드 차트 생성
    fig_trend = go.Figure()
    for stock, values in trend_data.items():
        fig_trend.add_trace(go.Scatter(x=['3개월 전', '2개월 전', '최근'], y=values, name=stock, mode='lines+markers'))
    fig_trend.update_layout(title="주요 종목 분배금 추이 (최근 3개월)", height=400)
    st.plotly_chart(fig_trend, use_container_width=True)

with col_t2:
    st.info("🤖 **AI 전략 코칭 (4월)**")
    st.markdown("""
    - **NVDY/PLTY:** 분배금 상승세 유지 중. **비중 확대 권장.**
    - **TSLY:** 분배금 역성장 및 주가 하락세. **비중 축소 후 QDTE로 이동 권장.**
    - **MSTY:** 변동성 확대 구간이나 배당 효율 최상. **유지 권장.**
    """)

# [3] 시뮬레이션 로직 (영업일 기준 월 투자액 반영)
start_date = datetime(2026, 3, 31)
current_assets = 2514595 # 4월 18일 기준 업데이트된 실제 자산
data = []

temp_assets = current_assets
for i in range(22): 
    current_date = start_date + timedelta(days=i*30)
    dividend = temp_assets * avg_yield
    temp_assets = temp_assets + monthly_investment + dividend
    data.append([current_date.strftime("%Y-%m"), int(temp_assets), int(dividend)])

df_sim = pd.DataFrame(data, columns=["연월", "누적자산", "월분배금"])

# [4] 대시보드 지표 및 그래프
c1, c2, c3 = st.columns(3)
with c1: st.metric("현재 자산 (평가금)", f"{current_assets:,} 원")
with c2: 
    success_row = df_sim[df_sim["월분배금"] >= target_dividend]
    target_month = success_row["연월"].iloc[0] if not success_row.empty else "분석 불가"
    st.metric("목표 65만원 달성 예상", target_month)
with c3: st.metric("영업일 기준 월 투자액", f"{monthly_investment:,} 원", help="월 평균 21일 기준")

# [5] 종목별 배수 지침 테이블
st.subheader("📋 이번 달 전략적 투자 배분 (DCA 가이드)")
# 질문자님의 엑셀 데이터를 기반으로 한 배분 (Gemini 권장안 반영)
strategy_table = pd.DataFrame({
    "종목": ["NVDY", "TSLY", "MSTY", "CONY", "PLTY", "ULTY", "BITO", "SOXL", "TQQQ", "TSLL", "QDTE", "XDTE"],
    "전략": ["확대", "축소", "유지", "유지", "확대", "관망", "유지", "유지", "방어", "관망", "확대", "확대"],
    "일일 투자금 (원)": [5000, 3000, 4000, 2500, 5000, 1500, 2500, 1000, 3000, 500, 4000, 4000]
})
st.table(strategy_table)
