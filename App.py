import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------------------------
# 🌍 페이지 기본 설정
# ---------------------------
st.set_page_config(
    page_title="🌍 지구 키우기 - 환경 행동 게임",
    layout="wide",
    page_icon="🌱"
)

# ---------------------------
# 🌈 스타일 (CSS 커스터마이징)
# ---------------------------
st.markdown("""
    <style>
    /* 배경색 & 글씨 */
    .stApp {
        background: linear-gradient(180deg, #e0f7fa 0%, #f1f8e9 100%);
        color: #004d40;
    }

    /* 타이틀 예쁘게 */
    h1, h2, h3 {
        text-align: center;
        color: #00695c;
    }

    /* 버튼 스타일 */
    div.stButton > button {
        background-color: #4caf50;
        color: white;
        border-radius: 12px;
        padding: 0.6em 1.5em;
        font-size: 1.05em;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #66bb6a;
        transform: scale(1.05);
    }

    /* 카드형 박스 느낌 */
    .mission-box {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# 세션 상태 초기화
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "start"
if "score" not in st.session_state:
    st.session_state.score = 0
if "actions" not in st.session_state:
    st.session_state.actions = []

# 페이지 이동 함수
def go_to(page):
    st.session_state.page = page


# ---------------------------
# 🌎 데이터 불러오기
# ---------------------------
file_path = os.path.join(os.path.dirname(__file__), "TalkFile_World.csv.csv")
df = pd.read_csv(file_path)

# 최신 연도 선택
latest_year = df["year"].max()
latest_data = df[df["year"] == latest_year]
latest_data = latest_data[
    ["country", "iso_code", "year", "co2", "gdp", "population", "co2_per_capita"]
].dropna()

# 한글화
latest_data.rename(columns={
    "country": "국가",
    "iso_code": "ISO",
    "co2": "CO₂ 배출량(백만톤)",
    "co2_per_capita": "1인당 CO₂(톤)",
    "population": "인구(명)",
    "gdp": "GDP(달러)"
}, inplace=True)

# ---------------------------
# 🌍 첫 화면: 지구 현황 지도
# ---------------------------
if st.session_state.page == "start":
    st.markdown("<h1>🌍 지구 키우기 🌱💚</h1>", unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align:center; font-size:18px;'>
    전 세계 나라별 CO₂ 배출 현황을 살펴보고,  
    <b>당신의 작은 실천</b>으로 지구를 행복하게 만들어보세요 🌏
    </p>
    """, unsafe_allow_html=True)

    # 지도
    fig = px.choropleth(
        latest_data,
        locations="ISO",
        color="CO₂ 배출량(백만톤)",
        hover_name="국가",
        hover_data={
            "1인당 CO₂(톤)": True,
            "GDP(달러)": True,
            "인구(명)": True
        },
        color_continuous_scale="RdYlGn_r",
        title=f"📊 {latest_year}년 세계 CO₂ 배출 현황"
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        height=550,
        coloraxis_colorbar=dict(title="CO₂ 배출량(백만톤)")
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.markdown("<h3 style='text-align:center;'>🌱 이제 행동으로 옮겨볼까요?</h3>", unsafe_allow_html=True)
    st.button("💪 환경 실천하러 가기", on_click=go_to, args=("action",))


# ---------------------------
# 🌿 환경 행동 화면
# ---------------------------
elif st.session_state.page == "action":
    st.markdown("<h2>🌱 환경 실천으로 지구를 행복하게 해주세요!</h2>", unsafe_allow_html=True)
    st.write("클릭할 때마다 지구의 행복도가 올라갑니다 💚")

    actions_dict = {
        "분리수거 ♻️ (+5)": 5,
        "텀블러 사용 ☕ (+3)": 3,
        "대중교통 이용 🚌 (+4)": 4,
        "일회용품 줄이기 🛍️ (+5)": 5,
        "절전 모드 사용 💡 (+2)": 2,
    }

    cols = st.columns(len(actions_dict))
    for i, (action, points) in enumerate(actions_dict.items()):
        with cols[i]:
            if st.button(action):
                st.session_state.score += points
                st.session_state.actions.append(action.split(" ")[0])
                st.balloons()
                st.success(f"{action.split()[0]} 실천 완료! 💚")

    st.divider()
    st.subheader(f"현재 점수: {st.session_state.score}")
    happiness = min(st.session_state.score / 50, 1.0)
    st.progress(happiness)

    # 지구 감정 변화
    st.markdown("<h3>🌍 지구 감정 상태</h3>", unsafe_allow_html=True)
    if happiness < 0.3:
        st.markdown("😢 슬퍼하는 지구... 구름이 낀 하늘 ☁️")
    elif happiness < 0.7:
        st.markdown("🙂 조금 괜찮아진 지구... 햇살이 비치기 시작해요 🌤️")
    else:
        st.markdown("😁🌿💚 행복한 지구! 무지개가 떴어요! 🌈💃🎉")

    st.divider()
    st.button("📋 행동 기록 & 미션 보기", on_click=go_to, args=("mission",))


# ---------------------------
# 🎯 미션 & 기록 화면
# ---------------------------
elif st.session_state.page == "mission":
    st.markdown("<h2>✅ 오늘의 기록 & 미션</h2>", unsafe_allow_html=True)

    with st.container():
        st.markdown("### 🌿 오늘 실천한 행동")
        if st.session_state.actions:
            for i, act in enumerate(st.session_state.actions, 1):
                st.markdown(f"<div class='mission-box'>{i}. {act} ✅</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='mission-box'>아직 실천한 행동이 없어요 🌱</div>", unsafe_allow_html=True)

        st.markdown("### 🎯 오늘의 환경 미션")
        missions = [
            "플라스틱 컵 1개 줄이기 🥤❌",
            "전기 사용 1시간 줄이기 💡⚡",
            "텀블러로 음료 마시기 ☕🌿",
            "분리수거 철저히 하기 ♻️💚",
            "가까운 거리 걸어가기 🚶‍♀️🚶‍♂️"
        ]
        today_mission = missions[st.session_state.score % len(missions)]
        st.markdown(f"<div class='mission-box'><b>{today_mission}</b></div>", unsafe_allow_html=True)

    st.divider()
    st.button("🏠 처음으로 돌아가기", on_click=go_to, args=("start",))
