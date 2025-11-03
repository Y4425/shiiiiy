# App.py
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
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────
# 세션 상태 초기화
# ──────────────────────────────
ss = st.session_state
for k,v in {"page":"start","score":0,"actions":[],"streak":0,"last_ts":0.0}.items():
    ss.setdefault(k,v)

def go_to(p): ss.page=p
def reset_game():
    for k in ["score","actions","streak","last_ts"]: ss[k]=0 if k!="actions" else []
    ss.page="start"

# ──────────────────────────────
# 기본 데이터 (세계 탄소배출)
# ──────────────────────────────
df = pd.DataFrame({
  "국가":["중국","미국","인도","러시아","일본","독일","이란","한국","인도네시아","캐나다"],
  "ISO":["CHN","USA","IND","RUS","JPN","DEU","IRN","KOR","IDN","CAN"],
  "CO2(억 톤)":[100,50,30,18,12,8,8,7,7,6]
})
df["세계비중(%)"]=(df["CO2(억 톤)"]/df["CO2(억 톤)"].sum()*100).round(1)
df["순위"]=df.index+1

# ──────────────────────────────
# 유틸 함수
# ──────────────────────────────
def happiness(score): return float(np.clip(score/60.0,0,1))
def mood_class(h): return "sad" if h<.25 else "neutral" if h<.55 else "happy" if h<.85 else "ecstatic"
def spin_speed(h): return f"{max(20-int(h*10)*2,8)}s"
def earth_size(h): return f"{int(200+h*70)}px"

def render_earth(h):
    cls=mood_class(h);size=earth_size(h);spin=spin_speed(h)
    html=f"""
    <div class="earth-wrap">
      <div class="earth {cls}" style="--size:{size};--spin:{spin}">
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
    st.markdown(html,unsafe_allow_html=True)
    txt={"sad":"지구가 힘들어해요… 행동이 필요해요.",
         "neutral":"지구가 조금 안정됐어요.",
         "happy":"지구가 미소 짓고 있어요! 💚",
         "ecstatic":"지구가 춤춰요! 💃✨"}[cls]
    st.markdown(f'<div class="status-text {cls}">{txt}</div>',unsafe_allow_html=True)

# ──────────────────────────────
# 행동 점수 반영
# ──────────────────────────────
def apply_action(points,label,is_good=True):
    now=time.time()
    if is_good:
        if ss.last_ts and now-ss.last_ts<=8: ss.streak+=1
        else: ss.streak=1
        bonus=max(0,ss.streak-2)
        ss.score=max(0,ss.score+points+bonus)
        st.balloons();st.success(f"{label} +{points}점 (콤보 {ss.streak}타, 보너스 +{bonus})")
    else:
        ss.streak=0;lost=abs(points);ss.score=max(0,ss.score-lost)
        st.error(f"{label} -{lost}점")
    ss.actions.append(label);ss.last_ts=now

# ──────────────────────────────
# 화면 구성
# ──────────────────────────────
if ss.page=="start":
    st.title("🌍 지구 키우기 — 환경오염의 심각성부터 보기")
    st.markdown("국가별 **CO₂ 배출량**을 확인하고, 작은 실천으로 지구를 행복하게 만들어봐요 🌱")
    c1,c2=st.columns([0.62,0.38])
    with c1:
        fig=px.choropleth(df,locations="ISO",color="CO2(억 톤)",
            hover_name="국가",hover_data=["세계비중(%)","순위"],
            color_continuous_scale="Reds",labels={"CO2(억 톤)":"CO₂(억 톤)"},
            projection="natural earth")
        fig.update_layout(height=470,margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown('<div class="glass">',unsafe_allow_html=True)
        sel=st.selectbox("국가 선택",df["국가"])
        row=df.loc[df["국가"]==sel].iloc[0]
        st.subheader(f"🔍 {row['국가']} 상세")
        a,b,c=st.columns(3)
        a.metric("CO₂(억 톤)",f"{row['CO2(억 톤)']}");b.metric("세계비중",f"{row['세계비중(%)']}%");c.metric("순위",row["순위"])
        st.markdown('</div>',unsafe_allow_html=True)
    st.divider()
    st.button("🌱 환경 실천하러 가기",on_click=go_to,args=("action",))

elif ss.page=="action":
    st.header("🌱 환경 행동으로 지구를 행복하게 해주세요!")
    good={"분리수거 ♻️":5,"텀블러 사용 ☕":3,"대중교통 이용 🚌":4,"일회용품 줄이기 🛍️":5,"계단 이용 🚶":2}
    bad={"차 혼자 타기 🚗":-5,"에어컨 빵빵 ❄️":-4,"일회용 빨대 사용 🥤":-2}
    st.subheader("✅ 좋은 행동");cols=st.columns(len(good))
    for (l,p),col in zip(good.items(),cols):
        with col:
            if st.button(f"{l} (+{p})",use_container_width=True): apply_action(p,l,True)
    st.subheader("⚠️ 나쁜 행동");cols=st.columns(len(bad))
    for (l,p),col in zip(bad.items(),cols):
        with col:
            if st.button(f"{l} ({p})",use_container_width=True): apply_action(p,l,False)
    h=happiness(ss.score)
    st.subheader(f"현재 점수: {ss.score} | 콤보: {ss.streak}타")
    st.progress(h,text="지구 행복도")
    render_earth(h)
    c1,c2=st.columns(2)
    with c1: st.button("📋 행동 기록 & 미션 보기",on_click=go_to,args=("mission",),use_container_width=True)
    with c2: st.button("🏠 처음 화면으로",on_click=go_to,args=("start",),use_container_width=True)

elif ss.page=="mission":
    st.header("✅ 오늘 실천한 행동")
    st.markdown('<div class="glass">',unsafe_allow_html=True)
    if ss.actions:
        for i,a in enumerate(ss.actions,1): st.write(f"{i}. {a}")
    else: st.write("아직 실천한 행동이 없어요 🌱")
    st.markdown('</div>',unsafe_allow_html=True)
    st.header("🎯 오늘의 환경 미션")
    missions=["플라스틱 컵 줄이기 🥤❌","전기 사용 1시간 줄이기 💡⚡","텀블러로 음료 마시기 ☕🌿","분리수거 철저히 하기 ♻️💚","대중교통으로 이동하기 🚌"]
    st.info(f"오늘의 미션: {missions[ss.score%len(missions)]}")
    st.subheader("지금 지구 상태 미리보기")
    render_earth(happiness(ss.score))
    c1,c2=st.columns(2)
    with c1: st.button("🌱 더 실천하러 가기",on_click=go_to,args=("action",),use_container_width=True)
    with c2: st.button("🏠 처음 화면으로",on_click=go_to,args=("start",),use_container_width=True)
