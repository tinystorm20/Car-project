import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="Car Project Strategy Center v2.1", layout="wide")

st.title("🚀 Car Project 전략 관제 대시보드 v2.1")
st.markdown("---")

# [1] 데이터 및 설정 관리 (영업일 기준 재계산 반영)
AVG_TRADING_DAYS = 21 

st.sidebar.header("⚙️ 기본 투자 설정")
daily_budget = st.sidebar.number_input("일일 총 투자금 (원)", value=29500, step=500)
monthly_investment = daily_budget * AVG_TRADING_DAYS 
target_dividend = st.sidebar.number_input("목표 월 분배금 (원)", value=650000)
avg_yield = st.sidebar.slider("전체 포트폴리오 예상 월 수익률 (%)", 0.0, 5.0, 3.0, 0.1) / 100

# [2] 시뮬레이션 로직 (영업일 기준 월 투자액 반영)
start_date = datetime(2026, 3, 31)
current_assets = 2514595 # 4월 18일 기준 실제 데이터
sim_data = []

temp_assets = current_assets
for i in range(22): # 2027년 12월까지
    current_date = start_date + timedelta(days=i*30)
    dividend = temp_assets * avg_yield
    temp_assets = temp_assets + monthly_investment + dividend
    sim_data.append([current_date.strftime("%Y-%m"), int(temp_assets), int(dividend)])

df_sim = pd.DataFrame(sim_data, columns=["연월", "누적자산", "월분배금"])

# [3] 시각화 섹션: 과거 트렌드 vs 미래 시뮬레이션
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 주요 종목 분배금 추이 (과거 3개월)")
    # 분석용 히스토리 데이터
    trend_data = {
        "NVDY": [0.82, 0.85, 0.84],
        "PLTY": [0.40, 0.42, 0.45],
        "MSTY": [1.20, 1.45, 1.50],
        "QDTE": [0.30, 0.33, 0.35],
    }
    fig_trend = go.Figure()
    for stock, values in trend_data.items():
        fig_trend.add_trace(go.Scatter(x=['3개월 전', '2개월 전', '최근'], y=values, name=stock, mode='lines+markers'))
    fig_trend.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_trend, use_container_width=True)

with col_right:
    st.subheader("📊 전체 월별 분배금 시뮬레이션 (미래)")
    fig_sim = go.Figure()
    fig_sim.add_trace(go.Bar(x=df_sim["연월"], y=df_sim["월분배금"], name="예상 분배금", marker_color='indianred'))
    fig_sim.add_trace(go.Scatter(x=df_sim["연월"], y=[target_dividend]*len(df_sim), name="목표선", line=dict(color='royalblue', dash='dash')))
    fig_sim.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_sim, use_container_width=True)

# [4] 핵심 성과 지표 (KPI)
st.markdown("---")
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("현재 자산", f"{current_assets:,} 원")
with c2: 
    success_row = df_sim[df_sim["월분배금"] >= target_dividend]
    target_month = success_row["연월"].iloc[0] if not success_row.empty else "2027년 이후"
    st.metric("목표 달성 예상", target_month)
with c3: st.metric("월 투자액 (영업일 기준)", f"{monthly_investment:,} 원")
with c4: st.metric("목표 분배금", f"{target_dividend:,} 원")

# [5] 전략 제안 및 투자 지침
st.markdown("---")
col_strat, col_table = st.columns([1, 2])

with col_strat:
    st.info("🤖 **AI 전략 코칭 (4월)**")
    st.markdown("""
    1. **공격적 확대:** 분배금 우상향 중인 **NVDY, PLTY** 비중을 높여 현금 흐름을 극대화하세요.
    2. **방어력 강화:** 하락장 대비를 위해 **QDTE, XDTE** 합산 비중을 20%까지 끌어올릴 시점입니다.
    3. **재투자 전략:** 수령한 분배금은 **TQQQ**에 우선 투입하여 원금 회복력을 높이세요.
    """)

with col_table:
    st.subheader("📋 이번 달 종목별 매수 지침 (DCA)")
    strategy_table = pd.DataFrame({
        "종목": ["NVDY", "TSLY", "MSTY", "CONY", "PLTY", "ULTY", "BITO", "SOXL", "TQQQ", "TSLL", "QDTE", "XDTE"],
        "전략": ["확대", "축소", "유지", "유지", "확대", "관망", "유지", "유지", "방어", "관망", "확대", "확대"],
        "일일 투자금 (원)": [5000, 3000, 4000, 2500, 5000, 1500, 2500, 1000, 3000, 500, 4000, 4000]
    })
    st.table(strategy_table)
    
# [6] 시뮬레이션 상세 프로세스 표 (v2.2 추가)
st.markdown("---")
st.subheader("📝 목표 달성 시뮬레이션 상세 로그")
st.write("기초 자산에 월 투자금과 분배금을 더해 다음 달 기초 자산이 되는 과정을 보여줍니다.")

# 표 데이터 포맷팅 (가독성을 위해 천단위 콤마 추가)
df_display = df_sim.copy()
df_display["누적자산"] = df_display["누적자산"].apply(lambda x: f"{x:,} 원")
df_display["월분배금"] = df_display["월분배금"].apply(lambda x: f"{x:,} 원")

# 인덱스를 '연월'로 설정하여 보기 좋게 출력
st.dataframe(df_display.set_index("연월"), use_container_width=True)

st.caption("※ 본 시뮬레이션은 월 평균 영업일 21일 기준이며, 주가 변동을 제외한 분배금 재투자를 가정합니다.")
