# app.py
import os
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

# ─────────────────────────────────────────────────────────
# 🌍 페이지 기본 설정
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌍 지구 키우기 - 환경 행동 게임",
    layout="wide",
    page_icon="🌱"
)

# ─────────────────────────────────────────────────────────
# 🌈 스타일 (CSS 커스터마이징)
# ─────────────────────────────────────────────────────────
st.markdown("""
    <style>
    /* 배경색 & 글씨 */
    .stApp {
        background: linear-gradient(180deg, #e0f7fa 0%, #f1f8e9 100%);
        color: #004d40;
        font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"Apple SD Gothic Neo","Noto Sans KR","Malgun Gothic",sans-serif;
    }
    /* 카드 느낌의 박스 */
    .glass {
        background: rgba(255,255,255,0.55);
        backdrop-filter: blur(6px);
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 12px;
        padding: 16px;
    }
    /* 제목 이모지 크기 */
    h1, h2, h3 { line-height: 1.2; }
    </style>
""", unsafe_allow_html=True)

st.title("🌍 지구 키우기 - 환경 행동 게임")
st.caption("CSV의 내용을 지도 위 마커 툴팁에 보여주고, 색/크기/필터/투영법을 조절할 수 있어요.")

# ─────────────────────────────────────────────────────────
# 📁 데이터 불러오기
# ─────────────────────────────────────────────────────────
DEFAULT_PATH = "/mnt/data/TalkFile_World.csv.csv"

with st.sidebar:
    st.header("📁 데이터")
    uploaded = st.file_uploader("CSV 파일 업로드 (.csv)", type=["csv"])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        st.success("업로드한 CSV를 사용합니다.")
    elif os.path.exists(DEFAULT_PATH):
        df = pd.read_csv(DEFAULT_PATH)
        st.info(f"기본 파일 사용: {DEFAULT_PATH}")
    else:
        st.error("CSV를 업로드하거나 기본 경로에 파일을 두세요.")
        st.stop()

# 빈 DF 방지
if df.empty:
    st.warning("CSV에 데이터가 없습니다.")
    st.stop()

# ─────────────────────────────────────────────────────────
# 🔎 위도/경도/이름 컬럼 자동 감지
# ─────────────────────────────────────────────────────────
LAT_CANDS = ["lat", "latitude", "위도", "Lat", "Latitude"]
LON_CANDS = ["lon", "lng", "longitude", "경도", "Lon", "Longitude"]
NAME_CANDS = ["name", "country", "국가", "지역", "도시", "place", "Name", "Country"]

def find_first(candidates, columns):
    for c in candidates:
        if c in columns:
            return c
    return None

auto_lat = find_first(LAT_CANDS, df.columns)
auto_lon = find_first(LON_CANDS, df.columns)
auto_name = find_first(NAME_CANDS, df.columns)

with st.sidebar:
    st.header("🗺️ 위치 매핑")
    lat_col = st.selectbox("위도 컬럼(lat)", options=df.columns, index=(list(df.columns).index(auto_lat) if auto_lat in df.columns else 0))
    lon_col = st.selectbox("경도 컬럼(lon)", options=df.columns, index=(list(df.columns).index(auto_lon) if auto_lon in df.columns else 0))
    name_col = st.selectbox("이름/제목(선택)", options=["(없음)"] + list(df.columns),
                            index=(0 if auto_name is None else (list(df.columns).index(auto_name) + 1)))
    name_col = None if name_col == "(없음)" else name_col

# 필수 체크
if lat_col is None or lon_col is None:
    st.error("위도/경도 컬럼을 지정해 주세요.")
    st.stop()

# ─────────────────────────────────────────────────────────
# 🧮 컬럼 타입 분류
# ─────────────────────────────────────────────────────────
numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
text_cols = [c for c in df.columns if c not in numeric_cols]

# ─────────────────────────────────────────────────────────
# 🎛️ 시각화 옵션 (사이드바)
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🎛️ 시각화 옵션")
    projection = st.selectbox("지도 투영법", options=[
        "natural earth", "equirectangular", "orthographic", "mercator", "kavrayskiy7",
        "miller", "robinson", "sinusoidal"
    ], index=0)

    color_col = st.selectbox("색상 컬럼(선택)", options=["(없음)"] + list(df.columns), index=0)
    color_col = None if color_col == "(없음)" else color_col

    size_col = st.selectbox("마커 크기 컬럼(선택, 숫자형 권장)", options=["(없음)"] + numeric_cols, index=0)
    size_col = None if size_col == "(없음)" else size_col

    default_size = 8
    min_size, max_size = st.slider("마커 크기 범위", 4, 40, (6, 14), help="size 컬럼이 없을 경우 가운데 값으로 그림")
    marker_size = (min_size + max_size) / 2 if size_col is None else None

# ─────────────────────────────────────────────────────────
# 🔧 데이터 필터 (사이드바)
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔎 데이터 필터")
    # 텍스트 필터
    search_col = st.selectbox("텍스트 검색 컬럼", options=["(없음)"] + text_cols, index=0)
    search_term = ""
    if search_col and search_col != "(없음)":
        search_term = st.text_input("포함할 키워드(부분일치)", value="")

    # 범주형/숫자 필터
    filter_col = st.selectbox("추가 필터 컬럼", options=["(없음)"] + list(df.columns), index=0)
    selected_vals = None
    num_range = None
    if filter_col and filter_col != "(없음)":
        if pd.api.types.is_numeric_dtype(df[filter_col]):
            col_min, col_max = float(np.nanmin(df[filter_col].values)), float(np.nanmax(df[filter_col].values))
            num_range = st.slider(f"{filter_col} 범위", float(col_min), float(col_max), (float(col_min), float(col_max)))
        else:
            uniq = sorted([str(x) for x in df[filter_col].dropna().unique().tolist()])
            selected_vals = st.multiselect(f"{filter_col} 값 선택", options=uniq, default=uniq)

# ─────────────────────────────────────────────────────────
# 🧹 필터 적용
# ─────────────────────────────────────────────────────────
df_view = df.copy()

# 텍스트 검색
if search_col and search_col != "(없음)" and search_term:
    df_view = df_view[df_view[search_col].astype(str).str.contains(search_term, case=False, na=False)]

# 숫자 범위 필터
if filter_col and filter_col != "(없음)":
    if pd.api.types.is_numeric_dtype(df_view[filter_col]):
        lo, hi = num_range
        df_view = df_view[(df_view[filter_col] >= lo) & (df_view[filter_col] <= hi)]
    else:
        if selected_vals is not None:
            df_view = df_view[df_view[filter_col].astype(str).isin(selected_vals)]

# 위/경도 결측 제거
df_view = df_view.dropna(subset=[lat_col, lon_col])

# 표시용 안내
with st.container():
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("📊 데이터 미리보기")
    st.dataframe(df_view.head(30), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# 🧰 툴팁 모드 선택: 기본 vs 고급(커스텀)
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🛠️ 툴팁 설정")
    tooltip_mode = st.radio("툴팁 모드", ["기본(자동)", "고급(커스텀)"], index=0)

# ─────────────────────────────────────────────────────────
# 🌐 지도 그리기: 기본(자동) 툴팁
# ─────────────────────────────────────────────────────────
def make_base_fig(dataframe):
    fig = px.scatter_geo(
        dataframe,
        lat=lat_col,
        lon=lon_col,
        hover_name=name_col if name_col else None,
        color=color_col if color_col else None,
        size=size_col if size_col else None,
        size_max=max_size,
        projection=projection
    )
    if size_col is None:
        fig.update_traces(marker=dict(size=marker_size))
    fig.update_geos(showcountries=True, showcoastlines=True)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=680)
    return fig

if tooltip_mode == "기본(자동)":
    exclude = {lat_col, lon_col}
    if name_col: exclude.add(name_col)
    hover_cols = [c for c in df_view.columns if c not in exclude]

    fig = make_base_fig(df_view)
    # NaN 예쁘게 처리
    df_auto = df_view.copy()
    df_auto[hover_cols] = df_auto[hover_cols].replace({np.nan: "-"})
    fig.update_traces(hovertemplate=None)  # PX 기본 툴팁 사용
    # PX의 hover_data를 강제하려면 다음처럼 새로 그림:
    fig = px.scatter_geo(
        df_auto,
        lat=lat_col,
        lon=lon_col,
        hover_name=name_col if name_col else None,
        hover_data=hover_cols,
        color=color_col if color_col else None,
        size=size_col if size_col else None,
        size_max=max_size,
        projection=projection
    )
    if size_col is None:
        fig.update_traces(marker=dict(size=marker_size))
    fig.update_geos(showcountries=True, showcoastlines=True)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=680)

    st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────────────────
# 🌐 지도 그리기: 고급(커스텀) 툴팁
# ─────────────────────────────────────────────────────────
else:
    st.markdown("#### ⚙️ 고급 툴팁 구성")
    # 순서 지정
    candidate_cols = [c for c in df_view.columns if c not in {lat_col, lon_col}]
    # 기본값: name_col이 있으면 맨 앞에, 이후 상위 4개
    default_order = []
    if name_col and name_col in candidate_cols:
        default_order.append(name_col)
    default_order += [c for c in candidate_cols if c != name_col][:5 - len(default_order)]
    cols_in_order = st.multiselect("툴팁에 표시할 컬럼(순서대로)", candidate_cols, default=default_order)

    if len(cols_in_order) == 0:
        st.warning("최소 1개 이상의 컬럼을 선택하세요.")
        st.stop()

    # NaN 처리
    df_tooltip = df_view.copy()
    df_tooltip[cols_in_order] = df_tooltip[cols_in_order].replace({np.nan: "-"})

    # 설정 폼
    st.write("각 컬럼별 라벨/단위/소수점 자릿수(숫자형만) 설정")
    labels, units, fmts = {}, {}, {}
    for c in cols_in_order:
        with st.container():
            cols = st.columns([2, 1, 1])
            labels[c] = cols[0].text_input(f"표시 라벨 - {c}", value=c, key=f"label_{c}")
            units[c] = cols[1].text_input("단위", value="", key=f"unit_{c}")
            if pd.api.types.is_numeric_dtype(df_tooltip[c]):
                decimals = cols[2].number_input("소수점 자리", 0, 6, 2, key=f"dec_{c}")
                fmts[c] = f":,.{int(decimals)}f"
            else:
                cols[2].markdown("&nbsp;")  # 자리 맞춤
                fmts[c] = ""

    # 도표 생성
    fig = make_base_fig(df_tooltip)

    # customdata & hovertemplate 구성
    customdata = df_tooltip[cols_in_order].values
    lines = []
    for i, c in enumerate(cols_in_order):
        label = labels[c]
        unit = units[c]
        fmt = fmts[c]  # '' 또는 ':,.2f' 같은 형태
        value_expr = f"%{{customdata[{i}]{fmt}}}" if fmt else f"%{{customdata[{i}]}}"
        # 이모지/불릿 등 자유롭게 바꿔도 됨
        line = f"• <b>{label}</b>: {value_expr}{unit}<br>"
        lines.append(line)
    hover_template = "".join(lines) + "<extra></extra>"

    fig.update_traces(customdata=customdata, hovertemplate=hover_template)
    st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────────────────
# ℹ️ 메타 정보
# ─────────────────────────────────────────────────────────
with st.expander("ℹ️ 현재 설정 / 도움말"):
    st.write("위도:", lat_col, " / 경도:", lon_col, " / 이름 컬럼:", name_col or "(없음)")
    st.write("색상 컬럼:", color_col or "(없음)", " / 크기 컬럼:", size_col or "(없음)")
    st.write(f"데이터 행 수(필터 적용): {len(df_view):,}")
    st.markdown("""
- **기본(자동) 툴팁**: 위도/경도(+이름)를 제외한 컬럼을 자동으로 모두 표시합니다.  
- **고급(커스텀) 툴팁**: `customdata + hovertemplate`로 원하는 컬럼/순서/라벨/단위/소수점 자릿수까지 제어합니다.  
- **팁**: 퍼센트는 원자료가 0~1 범위라면 100을 곱해 새로운 컬럼을 만들고 단위를 `%`로 지정하면 보기 좋아요.
""")
