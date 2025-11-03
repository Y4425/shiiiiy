# App.py
import os
import time
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ──────────────────────────────
# 페이지 기본 설정 + 스타일
# ──────────────────────────────
st.set_page_config(page_title="🌍 지구 키우기", layout="wide", page_icon="🌱")

# 🌈 CSS (배경 + 지구 디자인 + 효과)
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

/* 🌍 회전 지구 */
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
.status-text{font-size:26px;font-weight:800;text-align:center;margin-top:10px;}
.status-text.sad{color:var(--bad);}
.status-text.neutral{color:#00695c;}
.status-text.happy{color:var(--good);}
.status-text.ecstatic{color:#1b5e20;text-shadow:0 0 10px rgba(46,125,50,.25);}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────
# 세션 상태
# ──────────────────────────────
ss = st.session_state
for k, v in {"page": "start", "score": 0, "actions": []}.items():
    ss.setdefault(k, v)

def go_to(p): ss.page = p

# ──────────────────────────────
# 📁 CSV 자동 로드
# ──────────────────────────────
DEFAULT_PATH = "/mnt/data/TalkFile_World.csv.csv"
with st.sidebar:
    st.subheader("📊 데이터 파일")
    uploaded = st.file_uploader("CSV 업로드", type=["csv"])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        st.success("업로드한 CSV 사용 중")
    elif os.path.exists(DEFAULT_PATH):
        df = pd.read_csv(DEFAULT_PATH)
        st.info(f"기본 파일 사용: {DEFAULT_PATH}")
    else:
        st.error("CSV 파일이 필요합니다.")
        st.stop()

if df.empty:
    st.error("CSV가 비어 있습니다.")
    st.stop()

# ──────────────────────────────
# CSV 컬럼 자동 감지
# ──────────────────────────────
def pick_first(cands, cols):
    for c in cands:
        if c in cols: return c
    return None

def detect_schema(df):
    cols = list(df.columns)
    iso  = pick_first(["ISO","iso3","country_code","CountryCode"], cols)
    name = pick_first(["국가","나라","country","Country"], cols)
    co2  = pick_first(["CO2","배출","탄소"], cols)
    lat  = pick_first(["lat","위도","Latitude"], cols)
    lon  = pick_first(["lon","경도","Longitude"], cols)
    mode = "iso" if iso else ("latlon" if lat and lon else None)
    return {"mode":mode, "iso":iso, "name":name, "co2":co2, "lat":lat, "lon":lon}

# ──────────────────────────────
# 지구 렌더 함수
# ──────────────────────────────
def happiness(score): return float(np.clip(score/60.0,0,1))
def mood_class(h): return "sad" if h<.25 else "neutral" if h<.55 else "happy" if h<.85 else "ecstatic"

def render_earth(h):
    cls=mood_class(h)
    html=f"""
    <div class="earth-wrap">
      <div class="earth {cls}">
        <div class="ocean"></div><div class="land"></div>
        <div class="cloud"></div><div class="cloud cloud2"></div>
        <div class="face {cls}">
          <div class="eyes"><div class="eye"></div><div class="eye"></div></div>
          <div class="mouth"></div>
        </div>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    txt={"sad":"지구가 힘들어해요… 🥺","neutral":"지구가 조금 나아지고 있어요 🙂","happy":"지구가 미소 짓고 있어요! 💚","ecstatic":"지구가 춤춰요! 💃✨"}[cls]
    st.markdown(f'<div class="status-text {cls}">{txt}</div>', unsafe_allow_html=True)

# ──────────────────────────────
# 페이지: 시작 화면 (CSV 지도 + 탄소중립 목표)
# ──────────────────────────────
if ss.page=="start":
    st.title("🌍 지구 키우기 — 환경오염의 심각성부터 보기")

    meta = detect_schema(df)
    c1, c2 = st.columns([0.62,0.38], gap="large")

    with c1:
        if meta["mode"] == "iso":
            fig = px.choropleth(
                df,
                locations=meta["iso"],
                locationmode="ISO-3",
                color=meta["co2"] if meta["co2"] else None,
                hover_name=meta["name"] if meta["name"] else None,
                hover_data=[c for c in df.columns if c not in [meta["iso"]]],
                color_continuous_scale="Reds",
                labels={meta["co2"]:"CO₂ 배출" if meta["co2"] else "값"},
                projection="natural earth"
            )
        else:
            fig = px.scatter_geo(
                df,
                lat=meta["lat"], lon=meta["lon"],
                hover_name=meta["name"] if meta["name"] else None,
                hover_data=[c for c in df.columns if c not in [meta["lat"],meta["lon"]]],
            )
            fig.update_traces(marker=dict(size=8))

        fig.update_layout(height=470, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("🎯 탄소중립 목표")
        st.write("• **2030년 목표:** 탄소 배출 40% 감축")
        st.write("• **2050년 목표:** 완전 탄소중립 (Net Zero)")
        if meta["co2"] and pd.api.types.is_numeric_dtype(df[meta["co2"]]):
            total = df[meta["co2"]].sum()
            st.metric("총 배출량", f"{total:,.0f}")
        else:
            st.write("배출량 데이터가 숫자가 아니거나 누락되었습니다.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.button("🌱 환경 실천하러 가기", on_click=go_to, args=("action",))

# ──────────────────────────────
# 페이지: 행동 화면 (점수 + 지구 반응)
# ──────────────────────────────
elif ss.page=="action":
    st.header("🌱 환경 행동으로 지구를 행복하게 해주세요!")

    acts = {"분리수거 ♻️":5, "텀블러 사용 ☕":3, "대중교통 이용 🚌":4, "일회용품 줄이기 🛍️":5, "계단 이용 🚶":2}
    cols = st.columns(len(acts))
    for i, (label, pts) in enumerate(acts.items()):
        with cols[i]:
            if st.button(f"{label} (+{pts})"):
                ss.score += pts
                ss.actions.append(label)
                st.balloons()
                st.success(f"{label} 실천 완료! +{pts}점")

    st.subheader(f"현재 점수: {ss.score}")
    st.progress(happiness(ss.score), text="지구 행복도")
    render_earth(happiness(ss.score))

    st.button("🏠 처음 화면으로 돌아가기", on_click=go_to, args=("start",))
