# App.py
import os
import time
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ──────────────────────────────
# 페이지 기본 설정 + CSS
# ──────────────────────────────
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

/* 🌍 회전하는 지구 */
.earth-wrap{display:flex; align-items:center; justify-content:center; width:100%; margin:8px 0;}
.earth{position:relative; border-radius:50%; overflow:hidden;
  width:var(--size,220px); height:var(--size,220px);
  box-shadow:0 22px 44px rgba(0,0,0,.16), inset -14px -14px 24px rgba(0,0,0,.12);
  animation: spin var(--spin,16s) linear infinite;
}
.ocean{position:absolute; inset:0; border-radius:50%;
  background:radial-gradient(60% 60% at 35% 35%, #7bd2ff 0%, #42b6ea 25%, #168dd6 60%, #0a6bb5 100%);
}
.land,.land:before,.land:after{
  position:absolute; content:""; background:#49b675; border-radius:40% 60% 55% 45% / 50% 45% 55% 50%; opacity:.95;
}
.land{width:56%; height:36%; left:10%; top:22%; transform:rotate(-8deg);}
.land:before{width:28%; height:20%; left:62%; top:-8%; transform:rotate(12deg);}
.land:after{width:35%; height:22%; left:58%; top:55%; transform:rotate(-18deg);}

/* 구름 */
.cloud,.cloud:before{position:absolute; content:""; background:linear-gradient(#fff,#f6f6f6); border-radius:999px; opacity:.82;}
.cloud{width:48%; height:16%; left:-50%; top:28%; animation: drift 16s linear infinite;}
.cloud:before{width:36%; height:12%; left:40%; top:-24%;}
.cloud2{width:36%; height:12%; left:120%; top:58%; animation: drift2 22s linear infinite;}
@keyframes drift{from{transform:translateX(0)}to{transform:translateX(220%)}}
@keyframes drift2{from{transform:translateX(0)}to{transform:translateX(-260%)}}
@keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}

/* 표정 */
.face{position:absolute; inset:0;}
.eyes{position:absolute; top:42%; left:50%; width:52%; height:28%; transform:translateX(-50%); display:flex; justify-content:space-between; padding:0 16%;}
.eye{width:16px; height:16px; background:#1e2a2a; border-radius:50%;}
.mouth{position:absolute; top:60%; left:50%; transform:translateX(-50%); width:44%; height:28px;}
.mouth:before{content:""; position:absolute; inset:0; background:#1e2a2a; height:10px; border-radius:0 0 60px 60px / 0 0 50px 50px; transition:.35s;}
.sad .mouth:before{height:12px; border-radius:60px 60px 0 0 / 50px 50px 0 0; transform:rotate(180deg);}
.happy .mouth:before{height:18px;}
.ecstatic .mouth:before{height:26px;}
.earth.happy{box-shadow:0 24px 46px rgba(0,0,0,.18),0 0 0 8px rgba(46,125,50,.10) inset;}
.earth.ecstatic{box-shadow:0 28px 52px rgba(0,0,0,.2),0 0 0 10px rgba(46,125,50,.16) inset; animation: spin var(--spin,10s) linear infinite;}

/* 반짝이는 별 */
.sky{position:relative; height:38px; margin-top:4px;}
.star{position:absolute; width:6px; height:6px; border-radius:50%; background:radial-gradient(#fff,rgba(255,255,255,.1)); animation: twinkle 1.6s ease-in-out infinite; opacity:.0;}
.star:nth-child(1){left:20%; animation-delay:.1s;}
.star:nth-child(2){left:38%; animation-delay:.5s;}
.star:nth-child(3){left:52%; animation-delay:.2s;}
.star:nth-child(4){left:66%; animation-delay:.9s;}
.star:nth-child(5){left:82%; animation-delay:.4s;}
@keyframes twinkle{0%,100%{opacity:0}50%{opacity:1;transform:scale(1.4)}}

/* 크고 선명한 상태 텍스트 */
.status-text{font-size:26px;font-weight:800;text-align:center;margin-top:10px;}
.status-text.sad{color:var(--bad);}
.status-text.neutral{color:#00695c;}
.status-text.happy{color:var(--good);}
.status-text.ecstatic{color:#1b5e20;text-shadow:0 0 10px rgba(46,125,50,.25);}

/* 🔔 즉각 효과: 축하/경고 배너 & 지구 이펙트 */
.banner{
  padding:12px 16px; border-radius:12px; font-weight:800; font-size:18px;
  margin:10px 0; display:flex; align-items:center; gap:8px;
}
.banner.good{background:#e8f5e9; color:#1b5e20; border:1px solid rgba(27,94,32,.25); box-shadow:0 0 0 6px rgba(27,94,32,.08) inset;}
.banner.bad{background:#ffebee; color:#b71c1c; border:1px solid rgba(183,28,28,.25); box-shadow:0 0 0 6px rgba(183,28,28,.08) inset;}

.earth.flash-good{animation: glowPulse .8s ease-in-out 0s 2;}
@keyframes glowPulse{
  0%,100%{box-shadow:0 22px 44px rgba(0,0,0,.16), 0 0 0 10px rgba(76,175,80,.0) inset;}
  50%{box-shadow:0 22px 44px rgba(0,0,0,.16), 0 0 0 14px rgba(76,175,80,.35) inset;}
}
.earth.flash-bad{animation: shake .35s ease-in-out 0s 3;}
@keyframes shake{
  0%,100%{transform:translateX(0) rotate(0deg)}
  25%{transform:translateX(-6px) rotate(-1.5deg)}
  50%{transform:translateX(6px) rotate(1.5deg)}
  75%{transform:translateX(-5px) rotate(-1deg)}
}

/* 배지 표시 */
.badge-wrap{display:flex; flex-wrap:wrap; gap:8px; margin:6px 0 12px;}
.badge{padding:6px 10px; border-radius:999px; font-weight:700; font-size:13px; border:1px solid rgba(0,0,0,.08);}
.badge.green{background:#e8f5e9; color:#1b5e20;}
.badge.blue{background:#e3f2fd; color:#0d47a1;}
.badge.gold{background:#fff8e1; color:#b36b00;}
.badge.pink{background:#fce4ec; color:#ad1457;}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────
# 세션 상태 초기화
# ──────────────────────────────
ss = st.session_state
defaults = {
    "page":"start", "score":0, "actions":[], "streak":0, "last_ts":0.0,
    "effect_until":0.0, "effect_type":None,
    "badges":[], "daily_target":20, "daily_achieved":False
}
for k,v in defaults.items():
    ss.setdefault(k,v)

def go_to(p): ss.page=p
def now_ts(): return time.time()

def reset_game():
    ss.page="start"; ss.score=0; ss.actions=[]; ss.streak=0
    ss.last_ts=0.0; ss.effect_until=0.0; ss.effect_type=None
    ss.badges=[]; ss.daily_achieved=False

# ──────────────────────────────
# ✅ CSV 로더 (업로드 > 기본 경로) + 컬럼 자동 감지
# ──────────────────────────────
with st.sidebar:
    st.subheader("📁 데이터 파일")
    uploaded = st.file_uploader("CSV 업로드", type=["csv"])

DEFAULT_PATH = "/mnt/data/TalkFile_World.csv.csv"
if uploaded is not None:
    df_raw = pd.read_csv(uploaded)
    st.sidebar.success("업로드한 CSV 사용 중")
elif os.path.exists(DEFAULT_PATH):
    df_raw = pd.read_csv(DEFAULT_PATH)
    st.sidebar.info(f"기본 파일 사용: {DEFAULT_PATH}")
else:
    st.sidebar.error("CSV 파일을 업로드하거나 기본 경로에 파일을 두세요.")
    st.stop()

if df_raw.empty:
    st.error("CSV가 비어 있습니다.")
    st.stop()

def pick_first(cands, cols):
    for c in cands:
        if c in cols: return c
    return None

def detect_schema(df):
    cols = list(df.columns)
    iso  = pick_first(["ISO","iso","iso3","Iso3","country_code","CountryCode"], cols)
    name = pick_first(["국가","나라","country","Country","name","Name"], cols)
    co2  = pick_first(["CO2","co2","CO₂","배출","배출량","탄소","탄소배출","CO2(억 톤)","CO2_억톤"], cols)
    lat  = pick_first(["lat","latitude","Lat","Latitude","위도"], cols)
    lon  = pick_first(["lon","lng","longitude","Lon","Longitude","경도"], cols)
    mode = "iso" if iso else ("latlon" if lat and lon else None)
    return {"mode":mode, "iso":iso, "name":name, "co2":co2, "lat":lat, "lon":lon}

meta = detect_schema(df_raw)

# df(앱 내부 공용) 정규화: 기존 코드가 기대하는 컬럼들로 맞춤
if meta["mode"] == "iso":
    df = pd.DataFrame()
    df["ISO"] = df_raw[meta["iso"]].astype(str)
    df["국가"] = df_raw[meta["name"]].astype(str) if meta["name"] else df["ISO"]
    # CO2가 숫자면 표준 컬럼으로 복사, 아니면 None
    if meta["co2"] and pd.api.types.is_numeric_dtype(df_raw[meta["co2"]]):
        df["CO2(억 톤)"] = pd.to_numeric(df_raw[meta["co2"]], errors="coerce").fillna(0)
        df = df.groupby(["ISO","국가"], as_index=False)["CO2(억 톤)"].sum()
        total = df["CO2(억 톤)"].sum()
        if total > 0:
            df["세계비중(%)"] = (df["CO2(억 톤)"]/total*100).round(1)
        else:
            df["세계비중(%)"] = 0.0
        df = df.sort_values("CO2(억 톤)", ascending=False).reset_index(drop=True)
        df["순위"] = df.index+1
    else:
        # CO2가 없거나 비수치면 기본 1값 부여(색상 없음), 비중/순위는 표시 안 함
        df["CO2(억 톤)"] = np.nan
        df["세계비중(%)"] = np.nan
        df["순위"] = np.nan
elif meta["mode"] == "latlon":
    # 좌표 기반 산점도용 데이터
    df = df_raw.copy()
else:
    st.error("CSV에서 ISO3 또는 위도/경도 컬럼을 찾지 못했어요.")
    st.stop()

# 전세계 총배출(기준) & 목표 계산 (가능할 때만)
if meta["mode"]=="iso" and pd.api.types.is_numeric_dtype(df["CO2(억 톤)"]):
    BASE_TOTAL = float(df["CO2(억 톤)"].sum())
else:
    BASE_TOTAL = np.nan
TARGET_2030_TOTAL = BASE_TOTAL*0.60 if pd.notnull(BASE_TOTAL) else np.nan
TARGET_2050_TOTAL = 0.0

def reduction_percent(score:int)->float:
    # 점수 60 -> 40% 감축으로 환산
    return float(np.clip(score/60.0*40.0, 0, 40))

# ──────────────────────────────
# 유틸 함수(행복도, 지구 렌더, 배너/효과, 배지)
# ──────────────────────────────
def happiness(score): return float(np.clip(score/60.0,0,1))
def mood_class(h): return "sad" if h<.25 else "neutral" if h<.55 else "happy" if h<.85 else "ecstatic"
def spin_speed(h): return f"{max(20-int(h*10)*2,8)}s"
def earth_size(h): return f"{int(200+h*70)}px"

def set_effect(kind:str, duration:float=2.0):
    ss.effect_type = kind
    ss.effect_until = now_ts() + duration

def render_banner(kind:str):
    if kind=="good":
        st.markdown('<div class="banner good">✨ 너무 좋아요! 지구가 환하게 빛나요!</div>', unsafe_allow_html=True)
    elif kind=="bad":
        st.markdown('<div class="banner bad">⚠️ 경고! 지구가 아파하고 있어요… 행동을 바꿔주세요.</div>', unsafe_allow_html=True)

def render_earth(h: float):
    cls=mood_class(h); size=earth_size(h); spin=spin_speed(h)
    extra = ""
    if ss.effect_type and ss.effect_until > now_ts():
        extra = " flash-good" if ss.effect_type=="good" else " flash-bad"
    html=f"""
    <div class="earth-wrap">
      <div class="earth {cls}{extra}" style="--size:{size};--spin:{spin}">
        <div class="ocean"></div><div class="land"></div>
        <div class="cloud"></div><div class="cloud cloud2"></div>
        <div class="face {cls}">
          <div class="eyes"><div class="eye"></div><div class="eye"></div></div>
          <div class="mouth"></div>
        </div>
      </div>
    </div>
    <div class="sky"><div class="star"></div><div class="star"></div><div class="star"></div><div class="star"></div><div class="star"></div></div>
    """
    st.markdown(html, unsafe_allow_html=True)
    txt={"sad":"지구가 힘들어해요… 행동이 필요해요.",
         "neutral":"지구가 조금 안정됐어요.",
         "happy":"지구가 미소 짓고 있어요! 💚",
         "ecstatic":"지구가 춤춰요! 💃✨"}[cls]
    st.markdown(f'<div class="status-text {cls}">{txt}</div>', unsafe_allow_html=True)

def show_tip(msg:str):
    try: st.toast(msg, icon="🌿")
    except Exception: st.info(msg)

def award_badge(code:str, label:str, color:str):
    if code not in ss.badges:
        ss.badges.append(code)
        show_tip(f"배지 획득! {label}")

def render_badges():
    if not ss.badges: return
    label_map={
        "score10":"첫걸음 10점 🌱","score30":"지구 친구 30점 💚","score60":"지구 영웅 60점 🌎",
        "combo3":"콤보 3타! ⚡","combo5":"콤보 5타!! 💥","daily":"오늘의 목표 달성 🎯"
    }
    st.write("🏅 배지")
    st.markdown('<div class="badge-wrap">', unsafe_allow_html=True)
    for code in ss.badges:
        cls = "green"
        if code in ["score30","combo3"]: cls="blue"
        if code in ["score60","combo5"]: cls="gold"
        if code in ["daily"]: cls="pink"
        st.markdown(f'<span class="badge {cls}">{label_map.get(code,code)}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def apply_action(points:int, label:str, is_good:bool, tip_msg:str=""):
    now = now_ts()
    if is_good:
        if ss.last_ts and now-ss.last_ts<=8: ss.streak+=1
        else: ss.streak=1
        bonus=max(0,ss.streak-2)
        ss.score=max(0, ss.score + points + bonus)
        set_effect("good",1.8)
        st.balloons()
        st.success(f"{label} +{points}점 (콤보 {ss.streak}타, 보너스 +{bonus})")
        if tip_msg: show_tip(tip_msg)
        if ss.streak>=3: award_badge("combo3","콤보 3타! ⚡","blue")
        if ss.streak>=5: award_badge("combo5","콤보 5타!! 💥","gold")
    else:
        ss.streak=0
        lost=abs(points)
        ss.score=max(0, ss.score - lost)
        set_effect("bad",1.4)
        st.error(f"{label} -{lost}점")
        if tip_msg: show_tip(tip_msg)

    ss.actions.append(label); ss.last_ts=now
    if ss.score>=10: award_badge("score10","첫걸음 10점 🌱","green")
    if ss.score>=30: award_badge("score30","지구 친구 30점 💚","blue")
    if ss.score>=60: award_badge("score60","지구 영웅 60점 🌎","gold")
    if (not ss.daily_achieved) and ss.score>=ss.daily_target:
        ss.daily_achieved=True
        award_badge("daily","오늘의 목표 달성 🎯","pink")
        set_effect("good",2.0)
        st.balloons()
        st.success("🎉 축하해요! 오늘의 목표를 달성했어요!")

# ──────────────────────────────
# 사이드바: 네비/초기화 + 세계 평균 감축률(가상)
# ──────────────────────────────
with st.sidebar:
    st.header("🧭 메뉴")
    choice=st.radio("화면 이동", ["시작 화면","행동 화면","기록/미션"],
                    index={"start":0,"action":1,"mission":2}[ss.page])
    ss.page={"시작 화면":"start","행동 화면":"action","기록/미션":"mission"}[choice]
    st.divider()
    world_avg = st.slider("전세계 평균 감축률(가상, %)", 0, 40, 18)
    st.caption("게임 비교용 가상 수치입니다. (0~40%)")
    st.divider()
    st.button("🔄 초기화", on_click=reset_game)

# ──────────────────────────────
# 화면: 시작 (CSV 지도 + 탄소중립 목표 + 국가 비교)
# ──────────────────────────────
if ss.page=="start":
    st.title("🌍 지구 키우기 — 환경오염의 심각성부터 보기")
    st.markdown("CSV의 데이터를 **지도에 표시**하고, **탄소중립 목표**와 **나의 감축 기여도**를 비교해요! 🌱")

    c1,c2 = st.columns([0.62,0.38], gap="large")

    with c1:
        if meta["mode"] == "iso":
            fig=px.choropleth(
                df, locations="ISO",
                color="CO2(억 톤)" if "CO2(억 톤)" in df.columns and pd.api.types.is_numeric_dtype(df["CO2(억 톤)"]) else None,
                hover_name="국가",
                hover_data=[c for c in df.columns if c not in ["ISO"]],
                color_continuous_scale="Reds",
                labels={"CO2(억 톤)":"CO₂(억 톤)"},
                projection="natural earth"
            )
        else:
            fig=px.scatter_geo(
                df, lat=meta["lat"], lon=meta["lon"],
                hover_name=meta["name"] if meta["name"] in df.columns else None,
                hover_data=[c for c in df.columns if c not in [meta["lat"],meta["lon"]]],
            )
            fig.update_traces(marker=dict(size=8))
        fig.update_layout(height=470, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("🎯 탄소중립 목표 (총배출 기준)")
        if pd.notnull(BASE_TOTAL):
            st.write(f"• **기준 총배출(합계)**: {BASE_TOTAL:,.0f}")
            st.write(f"• **2030 목표(전세계)**: -40% ⇒ **{TARGET_2030_TOTAL:,.0f}**")
            st.write("• **2050 목표**: Net Zero(0)")
        else:
            st.info("CSV에 총배출(숫자) 컬럼이 없어서 합계를 계산하지 않았어요.")

        my_red = reduction_percent(ss.score)
        st.write(f"**나의 감축률(게임)**: {my_red:.1f}%  |  **전세계 평균(가상)**: {world_avg}%")
        st.progress(my_red/40.0, text="2030 목표 대비 '나의' 진척도")

        if meta["mode"]=="iso":
            sel = st.selectbox("국가 선택", df["국가"])
            row = df[df["국가"]==sel].iloc[0]
            a,b,c = st.columns(3)
            a.metric("CO₂(억 톤)", f"{row['CO2(억 톤)']}" if "CO2(억 톤)" in df.columns else "―")
            b.metric("세계비중",  f"{row['세계비중(%)']}%" if "세계비중(%)" in df.columns else "―")
            c.metric("배출 순위",  int(row["순위"]) if "순위" in df.columns and pd.notnull(row["순위"]) else "―")
        else:
            st.caption("좌표 기반 데이터라 국가 상세 메트릭은 생략했어요. (원본 행 미리보기)")
            st.dataframe(df.head(20), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.button("🌱 환경 실천하러 가기", on_click=go_to, args=("action",))

# ──────────────────────────────
# 화면: 행동 (팁/배지/일일목표 + 지구 반응)
# ──────────────────────────────
elif ss.page=="action":
    st.header("🌱 환경 행동으로 지구를 행복하게 해주세요!")

    if ss.effect_type and ss.effect_until > now_ts():
        render_banner(ss.effect_type)

    good_actions = {
        "분리수거 ♻️": (5, "깨끗이 헹구고 분리하면 재활용률이 올라가요!"),
        "텀블러 사용 ☕": (3, "텀블러 1회 = 일회용 컵 1개 절감!"),
        "대중교통 이용 🚌": (4, "승용차 대비 탄소를 크게 줄일 수 있어요."),
        "일회용품 줄이기 🛍️": (5, "다회용이 곧 지구의 미소입니다!"),
        "계단 이용 🚶": (2, "전기 절약 + 건강은 덤!"),
    }
    bad_actions = {
        "차 혼자 타기 🚗": (-5, "가능하면 카풀·대중교통을 고려해요."),
        "에어컨 빵빵 ❄️": (-4, "적정온도(여름 26~28도) 유지가 좋아요."),
        "일회용 빨대 사용 🥤": (-2, "빨대 없이도 충분히 즐길 수 있어요!"),
    }

    st.subheader("✅ 좋은 행동")
    gcols = st.columns(len(good_actions))
    for (label, (pts, tip)), col in zip(good_actions.items(), gcols):
        with col:
            if st.button(f"{label} (+{pts})", use_container_width=True):
                apply_action(pts, label, True, tip)

    st.subheader("⚠️ 나쁜 행동")
    bcols = st.columns(len(bad_actions))
    for (label, (pts, tip)), col in zip(bad_actions.items(), bcols):
        with col:
            if st.button(f"{label} ({pts})", use_container_width=True):
                apply_action(pts, label, False, tip)

    h = happiness(ss.score)
    st.subheader(f"현재 점수: {ss.score} | 콤보: {ss.streak}타 | 오늘 목표: {ss.daily_target}점" + (" ✅" if ss.daily_achieved else ""))
    st.progress(h, text="지구 행복도")

    render_earth(h)
    render_badges()

    c1,c2 = st.columns(2)
    with c1: st.button("📋 행동 기록 & 미션 보기", on_click=go_to, args=("mission",), use_container_width=True)
    with c2: st.button("🏠 처음 화면으로", on_click=go_to, args=("start",), use_container_width=True)

# ──────────────────────────────
# 화면: 기록/미션 (+ 배지)
# ──────────────────────────────
elif ss.page=="mission":
    st.header("✅ 오늘 실천한 행동")
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    if ss.actions:
        for i,a in enumerate(ss.actions,1): st.write(f"{i}. {a}")
    else:
        st.write("아직 실천한 행동이 없어요 🌱")
    st.markdown('</div>', unsafe_allow_html=True)

    st.header("🎯 오늘의 환경 미션")
    missions=[
        "플라스틱 컵 줄이기 🥤❌",
        "전기 사용 1시간 줄이기 💡⚡",
        "텀블러로 음료 마시기 ☕🌿",
        "분리수거 철저히 하기 ♻️💚",
        "대중교통으로 이동하기 🚌"
    ]
    st.info(f"오늘의 미션: {missions[ss.score%len(missions)]}")

    st.subheader("🏅 내가 모은 배지")
    render_badges()

    st.subheader("지금 지구 상태 미리보기")
    render_earth(happiness(ss.score))

    c1,c2=st.columns(2)
    with c1: st.button("🌱 더 실천하러 가기", on_click=go_to, args=("action",), use_container_width=True)
    with c2: st.button("🏠 처음 화면으로", on_click=go_to, args=("start",), use_container_width=True)
