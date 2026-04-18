import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="Car Project Control Center", layout="wide")

st.title("🚀 Car Project 전략 관제 대시보드")
st.markdown("---")

# [1] 사이드바: 기본 설정
st.sidebar.header("⚙️ 기본 투자 설정")
daily_budget = st.sidebar.number_input("일일 총 투자금 (원)", value=29500, step=500)
monthly_investment = daily_budget * 30
target_dividend = st.sidebar.number_input("목표 월 분배금 (원)", value=650000)
avg_yield = st.sidebar.slider("예상 월 수익률 (%)", 0.0, 5.0, 3.0, 0.1) / 100

# [2] 종목별 비중 설정 (질문자님의 11개 종목)
st.sidebar.header("📊 종목별 배분 비중 (%)")
stocks = {
    "NVDY": 15, "PLTY": 17, "MSTY": 10, "CONY": 8, "TSLY": 10, 
    "ULTY": 7, "XDTE": 10, "QDTE": 10, "TQQQ": 7, "SOXL": 3, "TSLL/BITO": 3
}

updated_weights = {}
total_weight = 0
for stock, weight in stocks.items():
    updated_weights[stock] = st.sidebar.number_input(f"{stock} 비중", value=weight)
    total_weight += updated_weights[stock]

if total_weight != 100:
    st.sidebar.error(f"비중 합계가 {total_weight}%입니다. 100%로 맞춰주세요.")

# [3] 시뮬레이션 로직
start_date = datetime(2026, 3, 31)
current_assets = 2139301 # 3월 말 기준 실제 데이터
data = []

temp_assets = current_assets
for i in range(22): # 2027년 12월까지 약 22개월
    current_date = start_date + timedelta(days=i*30)
    dividend = temp_assets * avg_yield
    temp_assets = temp_assets + monthly_investment + dividend
    data.append([current_date.strftime("%Y-%m"), int(temp_assets), int(dividend)])

df_sim = pd.DataFrame(data, columns=["연월", "누적자산", "월분배금"])

# [4] 메인 화면 지표
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("현재 자산", f"{current_assets:,} 원")
with col2:
    target_month = df_sim[df_sim["월분배금"] >= target_dividend]["연월"].iloc[0] if any(df_sim["월분배금"] >= target_dividend) else "2027년 이후"
    st.metric("목표 달성 예상", target_month)
with col3:
    st.metric("월 투자액", f"{monthly_investment:,} 원")

# [5] 인터랙티브 차트
fig = go.Figure()
fig.add_trace(go.Bar(x=df_sim["연월"], y=df_sim["월분배금"], name="예상 분배금", marker_color='indianred'))
fig.add_trace(go.Scatter(x=df_sim["연월"], y=[target_dividend]*len(df_sim), name="목표선", line=dict(color='royalblue', dash='dash')))
fig.update_layout(title="월별 분배금 성장 추이", xaxis_title="연월", yaxis_title="금액 (원)")
st.plotly_chart(fig, use_container_width=True)

# [6] 종목별 상세 배분표
st.subheader("📋 이번 달 종목별 매수 지침")
df_strategy = pd.DataFrame({
    "종목": updated_weights.keys(),
    "비중 (%)": updated_weights.values(),
    "일일 투자금 (원)": [int(daily_budget * (w/100)) for w in updated_weights.values()]
})
st.table(df_strategy)
