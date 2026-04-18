import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="Car Project Strategy Center v2.3", layout="wide")

st.title("🚀 Car Project 전략 관제 대시보드 v2.3")
st.markdown("---")

# [1] 데이터 및 설정 관리
AVG_TRADING_DAYS = 21 

st.sidebar.header("⚙️ 기본 투자 설정")
daily_budget = st.sidebar.number_input("일일 총 투자금 (원)", value=29500, step=500)
monthly_investment = daily_budget * AVG_TRADING_DAYS 
target_dividend = st.sidebar.number_input("목표 월 분배금 (원)", value=650000)
avg_yield = st.sidebar.slider("전체 포트폴리오 예상 월 수익률 (%)", 0.0, 5.0, 3.0, 0.1) / 100

# [2] 정교화된 시뮬레이션 로직
# 오늘(4/18) 기준 실제 평가액
current_actual_assets = 2514595 
# 4월 남은 영업일 매수 예정액 (약 9일 가정: 29,500 * 9)
april_remaining_investment = daily_budget * 9 
# 4월 말 예상 자산 = 현재 자산 + 남은 투자금 + 4월 예상 분배금
april_dividend = current_actual_assets * avg_yield
april_end_assets = current_actual_assets + april_remaining_investment + april_dividend

sim_data = []
# 4월 데이터 먼저 삽입
sim_data.append(["2026-04", int(april_end_assets), int(april_dividend)])

# 5월(2026-05)부터 2027-12까지 시뮬레이션
temp_assets = april_end_assets
start_date = datetime(2026, 5, 1)

for i in range(20): # 20개월 (26.05 ~ 27.12)
    current_date = start_date + timedelta(days=i*31) # 월 단위 근사
    dividend = temp_assets * avg_yield
    temp_assets = temp_assets + monthly_investment + dividend
    sim_data.append([current_date.strftime("%Y-%m"), int(temp_assets), int(dividend)])

df_sim = pd.DataFrame(sim_data, columns=["연월", "누적자산", "월분배금"])

# [3] 시각화 및 지표 (기존 유지)
col_left, col_right = st.columns(2)
with col_left:
    st.subheader("📊 전체 월별 분배금 시뮬레이션 (미래)")
    fig_sim = go.Figure()
    fig_sim.add_trace(go.Bar(x=df_sim["연월"], y=df_sim["월분배금"], name="예상 분배금", marker_color='indianred'))
    fig_sim.add_trace(go.Scatter(x=df_sim["연월"], y=[target_dividend]*len(df_sim), name="목표선", line=dict(color='royalblue', dash='dash')))
    st.plotly_chart(fig_sim, use_container_width=True)

with col_right:
    st.subheader("📝 목표 달성 시뮬레이션 상세 로그")
    df_display = df_sim.copy()
    df_display["누적자산"] = df_display["누적자산"].apply(lambda x: f"{x:,} 원")
    df_display["월분배금"] = df_display["월분배금"].apply(lambda x: f"{x:,} 원")
    st.dataframe(df_display.set_index("연월"), height=400, use_container_width=True)

# [4] 핵심 성과 지표 (KPI)
st.markdown("---")
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("현재 실제 자산 (4/18)", f"{current_actual_assets:,} 원")
with c2: 
    success_row = df_sim[df_sim["월분배금"] >= target_dividend]
    target_month = success_row["연월"].iloc[0] if not success_row.empty else "2028년 이후"
    st.metric("목표 달성 예상", target_month)
with c3: st.metric("월 투자액 (영업일 기준)", f"{monthly_investment:,} 원")
with c4: st.metric("4월말 예상 자산", f"{int(april_end_assets):,} 원")

# [5] 종목별 상세 배분 (DCA 가이드)
st.subheader("📋 이번 달 종목별 매수 지침 (DCA)")
strategy_table = pd.DataFrame({
    "종목": ["NVDY", "TSLY", "MSTY", "CONY", "PLTY", "ULTY", "BITO", "SOXL", "TQQQ", "TSLL", "QDTE", "XDTE"],
    "전략": ["확대", "축소", "유지", "유지", "확대", "관망", "유지", "유지", "방어", "관망", "확대", "확대"],
    "일일 투자금 (원)": [5000, 3000, 4000, 2500, 5000, 1500, 2500, 1000, 3000, 500, 4000, 4000]
})
st.table(strategy_table)

# [6] 시뮬레이션 상세 로그 (v2.3 추가)
st.markdown("---")
st.subheader("📝 [6] 목표 달성 시뮬레이션 상세 로그")
st.write("기초 자산에 월 투자금과 분배금을 더해 다음 달 기초 자산이 되는 상세 프로세스입니다.")

# 로그 데이터 생성 및 포맷팅
log_list = []
temp_log_assets = current_actual_assets
# 4월 로그
log_list.append({
    "연월": "2026-04",
    "기초 자산": f"{int(current_actual_assets):,} 원",
    "월 투자금": f"{int(april_remaining_investment):,} 원",
    "월 분배금": f"{int(april_dividend):,} 원",
    "기말 자산": f"{int(april_end_assets):,} 원"
})

# 5월 이후 로그
temp_log_assets = april_end_assets
for i in range(20):
    curr_date = start_date + timedelta(days=i*31)
    div = temp_log_assets * avg_yield
    prev_assets = temp_log_assets
    temp_log_assets = temp_log_assets + monthly_investment + div
    log_list.append({
        "연월": curr_date.strftime("%Y-%m"),
        "기초 자산": f"{int(prev_assets):,} 원",
        "월 투자금": f"{int(monthly_investment):,} 원",
        "월 분배금": f"{int(div):,} 원",
        "기말 자산": f"{int(temp_log_assets):,} 원"
    })

df_log = pd.DataFrame(log_list)
st.dataframe(df_log.set_index("연월"), use_container_width=True)
