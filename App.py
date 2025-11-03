# App.py
import time
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ─────────────────────────────────────────
# 기본 설정 & 전역 스타일
# ─────────────────────────────────────────
st.set_page_config(page_title="🌍 지구 키우기", layout="wide", page_icon="🌱")
st.markdown("""
<style>
:root{
  --ink:#004d40; --glass:rgba(255,255,255,.65);
  --good:#2e7d32; --mid:#f9a825; --bad:#c62828;
}
*{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"Noto Sans KR","Apple SD Gothic Neo",sans-serif;}
.stApp{background:linear-gradient(180deg,#e0f7fa 0%,#f1f8e9 100%); color:var(--ink);}
.glass{background:var(--glass); backdrop-filter:blur(6px); border-radius:14px; padding:16px; border:1px solid rgba(0,0,0,.06); margin-bottom:12px;}
.center{text-align:center}
.big{font-size:64px; line-height:1}

/* ── 🌍 CSS Earth (이미지 없이) ───────────────────────── */
.earth-wrap{display:flex; align-items:center; justify-content:center; width:100%; margin:8px 0 2px;}
.earth{
  position:relative; width:var(--size,220px); height:var(--size,220px); border-radius:50%;
  box-shadow:0 22px 44px rgba(0,0,0,.16), inset -14px -14px 24px rgba(0,0,0,.12);
  overflow:hidden; transform: translateZ(0); animation: spin var(--spin,16s) linear infinite;
}
.ocean{position:absolute; inset:0; border-radius:50%;
  background:radial-gradient(60% 60% at 35% 35%, #7bd2ff 0%, #42b6ea 25%, #168dd6 60%, #0a6bb5 100%);
}
.land,.land:before,.land:after{
  position:absolute; content:""; background:#49b675; filter: drop-shadow(0 2px 0 rgba(0,0,0,.12));
  border-radius:40% 60% 55% 45% / 50% 45% 55% 50%; opacity:.95;
}
.land{ width:56%; height:36%; left:10%; top:22%; transform:rotate(-8deg); }
.land:before{ width:28%; height:20%; left:62%; top:-8%; transform:rotate(12deg);}
.land:after{ width:35%; height:22%; left:58%; top:55%; transform:rotate(-18deg); }

.cloud,.cloud:before{position:absolute; content:""; background:linear-gradient(#fff,#f6f6f6); border-radius:999px; opacity:.82;}
.cloud{ width:48%; height:16%; left:-50%; top:28%; animation: drift 16s linear infinite; filter: blur(.2px);}
.cloud:before{ width:36%; height:12%; left:40%; top:-24%;}
.cloud2{ width:36%; height:12%; left:120%; top:58%; animation: drift2 22s linear infinite; filter: blur(.2px);}
@keyframes drift{ from{transform:translateX(0)} to{transform:translateX(220%)}}
@keyframes drift2{ from{transform:translateX(0)} to{transform:translateX(-260%)}}
@keyframes spin{ from{transform:rotate(0deg)} to{transform:rotate(360deg)} }

.face{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; }
.eyes{ position:absolute; top:42%; left:50%; width:52%; height:28%; transform:translateX(-50%); display:flex; justify-content:space-between; padding:0 16%; }
.eye{ width:16px; height:16px; background:#1e2a2a; border-radius:50%; box-shadow:0 2px 0 rgba(255,255,255,.35) inset; }
.mouth{ position:absolute; top:60%; left:50%; transform:translateX(-50%); width:44%; height:28px; }
.mouth:before{ content:""; position:absolute; inset:0; border-radius:0 0 60px 60px / 0 0 50px 50px; background:#1e2a2a;
  height:10px; transition:all .35s cubic-bezier(.2,.8,.2,1);
}
.blushL,.blushR{ position:absolute; top:54%; width:22px; height:12px; background:rgba(255,105,97,.35); border-radius:999px; filter: blur(.5px); }
.blushL{ left:22%; } .blushR{ right:22%; }

/* 표정 단계 */
.sad .mouth:before{ height:12px; border-radius:60px 60px 0 0 / 50px 50px 0 0; transform: translateX(-50%) rotate(180deg);}
.neutral .mouth:before{ height:10px;}
.happy .mouth:before{ height:18px;}
.ecstatic .mouth:before{ height:26px;}
.earth.happy{ box-shadow:0 24px 46px rgba(0,0,0,.18), 0 0 0 8px rgba(46,125,50,.10) inset;}
.earth.ecstatic{ box-shadow:0 28px 52px rgba(0,0,0,.2), 0 0 0 10px rgba(46,125,50,.16) inset; animation: spin var(--spin,10s) linear infinite;}

/* 반짝이는 별 */
.sky{ position:relative; height:38px; margin-top:4px;}
.star{ position:absolute; width:6px; height:6px; border-radius:50%; background: radial-gradient(#fff, rgba(255,255,255,.1));
  animation: twinkle 1.6s ease-in-out infinite; opacity:.0;
}
.star:nth-child(1){ left:20%; animation-delay:.1s;}
.star:nth-child(2){ left:38%; animation-delay:.5s;}
.star:nth-child(3){ left:52%; animation-delay:.2s;}
.star:nth-child(4){ left:66%; animation-delay:.9s;}
.star:nth-child(5){ left:82%; animation-delay:.4s;}
@keyframes twinkle{ 0%,100%{opacity:0} 50%{opacity:1; transform:scale(1.4)} }

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 세션 상태
# ─────────────────────────────────────────
ss = st.session_state
if "page" not in ss: ss.page = "start"        # start → action → mission
if "score" not in ss: ss.score = 0
if "actions" not in ss: ss.actions = []
if "selected_iso" not in ss: ss.selected_iso = None
if "streak" not in ss: ss.streak = 0          # 콤보
if "last_ts" not in ss: ss.last_ts = 0.0      # 콤보 시간 기준

def go_to(p): ss.page = p
def reset_game():
    ss.page, ss.score, ss.actions, ss.selected_iso = "start", 0, [], None
    ss.streak, ss.last_ts = 0, 0.0

# 사이드바
with st.sidebar:
    st.header("🧭 메뉴")
    choice = st.radio("화면 이동", ["시작 화면", "행동 화면", "기록/미션"],
                      index={"start":0,"action":1,"mission":2}[ss.page])
    ss.page = {"시작 화면":"start","행동 화면":"action","기록/미션":"mission"}[choice]
    st.divider()
    st.button("🔄 초기화", on_click=reset_game)

# ─────────────────────────────────────────
# 데이터(옵션 업로드 또는 내장 예시)
# ─────────────────────────────────────────
with st.sidebar:
    st.subheader("📁 데이터")
    up = st.file_uploader("세계 CO₂ CSV (ISO3, 국가, CO2열 포함)", type=["csv"])
if up is not None:
    df = pd.read_csv(up)
    # 최소 컬럼 추정
    iso_col = next((c for c in df.columns if c.lower() in ["iso","iso3","country_code"]), None)
    name_col = next((c for c in df.columns if "국가" in c or c.lower() in ["name","country"]), None)
    co2_col = next((c for c in df.columns if "co2" in c.lower()), None)
    if not (iso_col and name_col and co2_col):
        st.warning("필요 컬럼(ISO/국가/CO2)을 찾지 못해 내장 예시 데이터로 대체합니다.")
        up = None

if up is None:
    df = pd.DataFrame({
        "국가":["중국","미국","인도","러시아","일본","독일","이란","한국","인도네시아","캐나다"],
        "ISO":["CHN","USA","IND","RUS","JPN","DEU","IRN","KOR","IDN","CAN"],
        "CO2(억 톤)":[100,50,30,18,12,8,8,7,7,6]
    })
    iso_col, name_col, co2_col = "ISO","국가","CO2(억 톤)"

df["세계비중(%)"] = (df[co2_col]/df[co2_col].sum()*100).round(1)
df = df.sort_values(co2_col, ascending=False).reset_index(drop=True)
df["순위"] = df.index + 1

# ─────────────────────────────────────────
# 행복도/표정/속도 계산
# ─────────────────────────────────────────
def happiness(score:int)->float:
    return float(np.clip(score/60.0, 0.0, 1.0))  # 만점 기준 60점

def mood_class(h:float)->str:
    if h < .25: return "sad"
    if h < .55: return "neutral"
    if h < .85: return "happy"
    return "ecstatic"

def spin_speed(h:float)->str:
    # 행복할수록 더 빨리(작은 초)
    return f"{max(20 - int(h*10)*2, 8)}s"

def earth_size(h:float)->str:
    # 행복할수록 살짝 커지도록
    base = 200
    size = int(base + h*70)  # 200px ~ 270px
    return f"{size}px"

def render_earth(h:float):
    cls = mood_class(h)
    size = earth_size(h)
    spin = spin_speed(h)
    html = f"""
    <div class="earth-wrap">
      <div class="earth {cls}" style="--size:{size}; --spin:{spin}">
        <div class="ocean"></div>
        <div class="land"></div>
        <div class="cloud"></div>
        <div class="cloud cloud2"></div>
        <div class="face {cls}">
          <div class="eyes"><div class="eye"></div><div class="eye"></div></div>
          <div class="mouth"></div>
          <div class="blushL"></div><div class="blushR"></div>
        </div>
      </div>
    </div>
    <div class="sky">
      <div class="star"></div><div class="star"></div><div class="star"></div><div class="star"></div><div class="star"></div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    if cls=="sad": st.caption("지구가 힘들어해요… 행동이 필요해요.")
    elif cls=="neutral": st.caption("지구가 조금 안정됐어요.")
    elif cls=="happy": st.caption("지구가 미소 짓고 있어요! 💚")
    else: st.caption("지구가 춤춰요! 💃✨")

# 콤보 계산: 8초 이내 연속 ‘좋은 행동’시 누적
def apply_action(points:int, label:str, is_good:bool):
    now = time.time()
    if is_good:
        if ss.last_ts and (now - ss.last_ts) <= 8:
            ss.streak += 1
        else:
            ss.streak = 1
        bonus = max(0, ss.streak - 2)   # 3타부터 +1, 4타부터 +2 …
        gained = points + bonus
        ss.score = max(0, ss.score + gained)
        st.balloons()
        st.success(f"{label} +{points}점  (콤보 {ss.streak}타, 보너스 +{bonus})")
    else:
        ss.streak = 0
        lost = abs(points)
        ss.score = max(0, ss.score - lost)
        st.error(f"{label} -{lost}점")
    ss.actions.append(label)
    ss.last_ts = now

# ─────────────────────────────────────────
# 시작 화면: 세계 탄소배출 지도 + 상세
# ─────────────────────────────────────────
if ss.page == "start":
    st.title("🌍 지구 키우기 — 환경오염의 심각성부터 보기")
    st.markdown("국가별 **CO₂ 배출량** 지도를 보고, 어떤 곳에서 많은 배출이 일어나는지 확인해요. 그다음 **환경 행동**으로 지구를 행복하게 만들어봐요! 🌱")

    c_map, c_detail = st.columns([0.62, 0.38], gap="large")
    with c_map:
        fig = px.choropleth(
            df, locations=iso_col, locationmode="ISO-3",
            color=co2_col, hover_name=name_col,
            hover_data=[co2_col,"세계비중(%)","순위"],
            color_continuous_scale="Reds",
            labels={co2_col:"CO₂ 배출(억 톤)"},
            projection="natural earth"
        )
        fig.update_layout(height=470, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with c_detail:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        sel = st.selectbox("국가 선택", options=df[name_col])
        row = df.loc[df[name_col]==sel].iloc[0]
        ss.selected_iso = row[iso_col]
        st.subheader(f"🔍 {row[name_col]} 상세")
        cA, cB, cC = st.columns(3)
        cA.metric("CO₂(억 톤)", f"{row[co2_col]}")
        cB.metric("세계 비중", f"{row['세계비중(%)']}%")
        cC.metric("배출 순위", int(row["순위"]))
        top = df.head(10)
        fig_bar = px.bar(top, x=name_col, y=co2_col, color=name_col)
        fig_bar.update_layout(showlegend=False, height=260, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.button("🌱 환경 실천하러 가기", on_click=go_to, args=("action",))

# ─────────────────────────────────────────
# 행동 화면: 좋은/나쁜 행동 + 콤보 + 지구 시각화
# ─────────────────────────────────────────
elif ss.page == "action":
    st.header("🌱 환경 행동으로 지구를 행복하게 해주세요!")

    good_actions = {
        "분리수거 ♻️":5, "텀블러 사용 ☕":3, "대중교통 이용 🚌":4,
        "일회용품 줄이기 🛍️":5, "계단 이용 🚶":2
    }
    bad_actions = {
        "차 혼자 타기 🚗":-5, "에어컨 빵빵 ❄️":-4, "일회용 빨대 사용 🥤":-2
    }

    st.subheader("✅ 좋은 행동")
    gcols = st.columns(len(good_actions))
    for i,(label,pts) in enumerate(good_actions.items()):
        with gcols[i]:
            if st.button(f"{label} (+{pts})", use_container_width=True):
                apply_action(pts, label, is_good=True)

    st.subheader("⚠️ 나쁜 행동")
    bcols = st.columns(len(bad_actions))
    for i,(label,pts) in enumerate(bad_actions.items()):
        with bcols[i]:
            if st.button(f"{label} ({pts})", use_container_width=True):
                apply_action(pts, label, is_good=False)

    h = happiness(ss.score)
    st.subheader(f"현재 점수: {ss.score}  |  콤보: {ss.streak}타")
    st.progress(h, text="지구 행복도")

    # 🌍 회전 속도/크기/표정이 행복도에 따라 바뀌는 지구
    render_earth(h)

    c1,c2 = st.columns(2)
    with c1: st.button("📋 행동 기록 & 미션 보기", on_click=go_to, args=("mission",), use_container_width=True)
    with c2: st.button("🏠 처음 화면으로", on_click=go_to, args=("start",), use_container_width=True)

# ─────────────────────────────────────────
# 기록/미션 화면
# ─────────────────────────────────────────
elif ss.page == "mission":
    st.header("✅ 오늘 실천한 행동 기록")
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    if ss.actions:
        for i,a in enumerate(ss.actions,1):
            st.write(f"{i}. {a}")
    else:
        st.write("아직 실천한 행동이 없어요 🌱")
    st.markdown('</div>', unsafe_allow_html=True)

    st.header("🎯 오늘의 환경 미션")
    missions = [
        "플라스틱 컵 1개 줄이기 🥤❌",
        "전기 사용 1시간 줄이기 💡⚡",
        "텀블러로 음료 마시기 ☕🌿",
        "분리수거 철저히 하기 ♻️💚",
        "대중교통으로 1회 이동하기 🚌"
    ]
    st.info(f"오늘의 미션: {missions[ss.score % len(missions)]}")

    st.subheader("지금 지구 상태 미리보기")
    render_earth(happiness(ss.score))

    c1,c2 = st.columns(2)
    with c1: st.button("🌱 더 실천하러 가기", on_click=go_to, args=("action",), use_container_width=True)
    with c2: st.button("🏠 처음 화면으로", on_click=go_to, args=("start",), use_container_width=True)
        
