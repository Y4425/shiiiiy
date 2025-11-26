import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import random

# -------------------------------------------------
# 기본 설정 & 공통 스타일
# -------------------------------------------------
st.set_page_config(
    page_title="데이터 가명처리 · 익명처리 · 동형암호 실습",
    layout="centered"
)

# 공통 CSS (배경, 카드, 버튼, 제목 스타일)
GLOBAL_CSS = """
<style>
body {
    background-color: #F4F5FB;
}

/* 메인 컨테이너 padding 약간 줄이기 */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
}

/* 카드 스타일 */
.card {
    background: #FFFFFF;
    padding: 20px 22px;
    border-radius: 18px;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08);
    margin-top: 12px;
    margin-bottom: 12px;
}

/* 섹션 제목 */
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #3949AB;
    margin-bottom: 0.3rem;
}

/* 작은 캡션 텍스트 */
.sub-caption {
    font-size: 0.86rem;
    color: #666666;
}

/* 버튼 */
.stButton > button {
    background: linear-gradient(90deg, #5C6BC0, #3949AB);
    color: white;
    border-radius: 999px;
    padding: 0.5rem 1.4rem;
    border: none;
    font-weight: 600;
}

/* k 표시 뱃지 */
.k-badge-small {
    background: #ffb3b3;
    padding: 4px 10px;
    border-radius: 999px;
    color: #8b0000;
    font-weight: 600;
    font-size: 0.85rem;
}
.k-badge-mid {
    background: #ffe6a1;
    padding: 4px 10px;
    border-radius: 999px;
    color: #8b6e00;
    font-weight: 600;
    font-size: 0.85rem;
}
.k-badge-good {
    background: #c9f7c5;
    padding: 4px 10px;
    border-radius: 999px;
    color: #0d6b00;
    font-weight: 600;
    font-size: 0.85rem;
}

/* 작은 라벨 느낌 텍스트 */
.label-chip {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    background: #E8EAF6;
    color: #283593;
    font-size: 0.8rem;
    font-weight: 600;
}

/* 코드 블록 폰트 조금 줄이기 */
code {
    font-size: 0.8rem !important;
}
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# -------------------------------------------------
# 상단 타이틀 영역
# -------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; margin-bottom: 1.2rem;">
        <div style="font-size:2.0rem; font-weight:800; color:#283593;">
            🧬 데이터 가명처리 · 익명처리 · 동형암호 실습
        </div>
        <div style="margin-top:0.4rem; font-size:0.95rem; color:#555;">
            개인정보 보호 기술(가명처리, 익명·비식별화, 동형암호 개념)을
            <b>직접 체험</b>해 볼 수 있는 교육용 웹앱입니다.
        </div>
        <div style="margin-top:0.3rem;">
            <span class="label-chip">코딩 동아리 프로젝트</span>
            <span class="label-chip">Python · Streamlit</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["1️⃣ 가명처리", "2️⃣ 익명·비식별화", "3️⃣ 동형암호(개념 실습)"])

# -------------------------------------------------
# 1. 가명처리 탭
# -------------------------------------------------
with tab1:
    st.markdown('<div class="section-title">1️⃣ 가명처리 (Pseudonymization) 실습</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="sub-caption">
        가명처리는 이름·주민번호·전화번호처럼 <b>직접 식별자</b>를  
        다른 값으로 치환해서 원래 누구였는지 알기 어렵게 만드는 기술입니다.
        (예: 이름 → 마스킹, 주민번호 → 해시 기반 가명 ID 등)
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("**🔑 원본 개인정보 입력**")
                name = st.text_input("이름", value="홍길동")
                rrn = st.text_input("주민번호(예시)", value="000101-3123456")
                phone = st.text_input("전화번호(예시)", value="010-1234-5678")
                st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**🧂 가명 ID 생성을 위한 비밀키 (salt)**")
            salt = st.text_input("비밀키(salt)", value="my_secret_key")
            st.caption("※ 같은 주민번호라도 salt가 다르면 다른 가명 ID가 생성됩니다.")
            st.markdown("</div>", unsafe_allow_html=True)

    # 마스킹 함수들
    def mask_name(n: str) -> str:
        if len(n) <= 1:
            return "*"
        return n[0] + "*" * (len(n) - 1)

    def mask_rrn(r: str) -> str:
        if len(r) >= 8:
            return r[:8] + "******"
        return r

    def mask_phone(p: str) -> str:
        if "-" in p:
            parts = p.split("-")
            if len(parts) == 3:
                return f"{parts[0]}-****-{parts[2]}"
        if len(p) > 4:
            return "*" * (len(p) - 4) + p[-4:]
        return p

    def make_pseudo_id(text: str, salt: str = "") -> str:
        base = (text + salt).encode("utf-8")
        return hashlib.sha256(base).hexdigest()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    if st.button("🔐 가명처리 실행하기"):
        masked_name = mask_name(name)
        masked_rrn = mask_rrn(rrn)
        masked_phone = mask_phone(콜)
        pseudo_id = make_pseudo_id(rrn + phone, salt)

        result_df = pd.DataFrame(
            {
                "항목": ["이름", "주민번호", "전화번호", "가명 ID(해시)"],
                "원본 값": [name, rrn, phone, "(원본 값을 직접 저장하지 않음)"],
                "가명/마스킹 결과": [
                    masked_name,
                    masked_rrn,
                    masked_phone,
                    pseudo_id[:16] + "...",
                ],
            }
        )

        st.success("가명처리 결과입니다.")
        st.dataframe(result_df, use_container_width=True)

        st.info(
            "실제 시스템에서는 주민번호·전화번호를 그대로 저장하지 않고, "
            "이런 해시 기반 가명 ID만 보관하여 유출 위험을 줄입니다."
        )
    else:
        st.caption("버튼을 눌러 가명처리 결과를 확인해 보세요.")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# 2. 익명·비식별화 탭 (k-익명성 + 디자인 개선)
# -------------------------------------------------
with tab2:
    st.markdown('<div class="section-title">2️⃣ 익명·비식별화 (k-Anonymity)</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="sub-caption">
        익명·비식별화는 데이터는 남기되,  
        <b>개인이 누구인지 재식별하기 어렵도록</b> 정보를 일반화/삭제하는 과정입니다.  
        여기서는 <b>나이 구간</b>과 <b>우편번호 앞자리</b>를 조절하면서
        <span style="font-weight:600;">k-익명성</span>을 직관적으로 확인해 봅니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 예시 데이터
    raw_data = pd.DataFrame(
        {
            "나이": [23, 25, 27, 34, 36, 42, 44, 52, 55, 60],
            "우편번호": [
                "12345",
                "12340",
                "12347",
                "12390",
                "12410",
                "12500",
                "12503",
                "12780",
                "12782",
                "12900",
            ],
            "질병": ["감기", "독감", "우울증", "감기", "당뇨", "고혈압", "감기", "우울증", "감기", "암"],
        }
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**🔍 원본 데이터 (작은 의료 데이터 예시)**")
    st.dataframe(raw_data, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 설정 카드
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**⚙️ 익명화 설정**")

    col_a, col_b = st.columns(2)
    with col_a:
        age_group_size = st.slider(
            "나이 구간 크기 (예: 10살 단위)",
            min_value=5,
            max_value=20,
            value=10,
            step=5,
        )
    with col_b:
        zip_keep = st.slider(
            "우편번호 앞에서부터 보존할 자리 수",
            min_value=1,
            max_value=5,
            value=3,
        )
    st.caption("※ 구간을 넓게, 우편번호 자릿수를 줄일수록 k 값이 커지는 경향이 있습니다.")
    st.markdown("</div>", unsafe_allow_html=True)

    # 일반화 함수
    def generalize_age(age: int, group_size: int) -> str:
        base = (age // group_size) * group_size
        return f"{base}~{base + group_size - 1}"

    def generalize_zip(zipcode: str, keep: int) -> str:
        if len(zipcode) <= keep:
            return zipcode
        return zipcode[:keep] + "*" * (len(zipcode) - keep)

    # 1차 일반화
    anon_df = raw_data.copy()
    anon_df["나이_구간"] = anon_df["나이"].apply(lambda x: generalize_age(x, age_group_size))
    anon_df["우편번호_일반화"] = anon_df["우편번호"].apply(lambda x: generalize_zip(x, zip_keep))

    group_cols = ["나이_구간", "우편번호_일반화"]
    group_k = (
        anon_df.groupby(group_cols)
        .size()
        .reset_index(name="k")
        .sort_values("k", ascending=False)
    )
    min_k = int(group_k["k"].min())

    # k가 너무 작으면 자동 보정
    target_k = 3  # 최소 3-익명성 이상을 기본 목표
    auto_adjusted = False
    if min_k < target_k:
        auto_adjusted = True
        # 나이 구간 키우고, 우편번호 자릿수 줄이기
        age_group_size = max(age_group_size, 15)
        zip_keep = min(zip_keep, 2)

        # 다시 일반화
        anon_df["나이_구간"] = anon_df["나이"].apply(lambda x: generalize_age(x, age_group_size))
        anon_df["우편번호_일반화"] = anon_df["우편번호"].apply(lambda x: generalize_zip(x, zip_keep))
        group_k = (
            anon_df.groupby(group_cols)
            .size()
            .reset_index(name="k")
            .sort_values("k", ascending=False)
        )
        min_k = int(group_k["k"].min())

    # 결과 카드들
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**🎨 익명화(일반화) 결과 – 그룹별 k 값**")

    if auto_adjusted:
        st.warning(
            f"초기 설정에서 최소 k 값이 너무 작아 자동으로 값을 조정했습니다.\n"
            f"→ 나이 구간: {age_group_size}살 단위, 우편번호 앞 {zip_keep}자리만 사용"
        )

    for _, row in group_k.iterrows():
        k = int(row["k"])
        age_r = row["나이_구간"]
        zip_r = row["우편번호_일반화"]

        if k < 3:
            badge = f"<span class='k-badge-small'>k={k}</span>"
        elif k < 5:
            badge = f"<span class='k-badge-mid'>k={k}</span>"
        else:
            badge = f"<span class='k-badge-good'>k={k}</span>"

        st.markdown(
            f"""
            <div style="margin-bottom:8px;">
                <b>나이 구간:</b> {age_r} &nbsp; | &nbsp;
                <b>우편번호:</b> {zip_r} &nbsp; | &nbsp;
                <b>그룹 크기:</b> {badge}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.success(f"🔒 최종 최소 k 값: **{min_k}** (k가 클수록 재식별 위험이 낮습니다)")
    with st.expander("📊 익명화된 상세 데이터 테이블도 보고 싶다면 열어보기"):
        st.dataframe(
            anon_df[["나이_구간", "우편번호_일반화", "질병"]],
            use_container_width=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# 3. 동형암호(개념 실습) 탭
# -------------------------------------------------
with tab3:
    st.markdown('<div class="section-title">3️⃣ 동형암호 개념 실습 (장난감 예시)</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="sub-caption">
        동형암호(Homomorphic Encryption)는 <b>암호화된 상태 그대로</b>  
        덧셈·곱셈 같은 연산을 할 수 있게 해 주는 암호입니다.  
        여기서는 수학적으로 직관을 잡기 위한 <b>아주 단순한 장난감 모델</b>을 사용합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**1️⃣ 키와 평문 값 설정**")

    key = st.slider("암호 키 K (충분히 큰 정수)", min_value=50, max_value=300, value=101, step=1)
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        m1 = st.number_input("첫 번째 평문 값 m1", min_value=0, max_value=20, value=5, step=1)
    with col_m2:
        m2 = st.number_input("두 번째 평문 값 m2", min_value=0, max_value=20, value=7, step=1)

    st.caption("※ 조건: m1 + m2 < K 범위 안에 있을수록 정확히 동작합니다.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    if st.button("🧮 동형암호(장난감) 연산 시뮬레이션"):
        r1 = random.randint(1, 10)
        r2 = random.randint(1, 10)

        C1 = m1 + r1 * key
        C2 = m2 + r2 * key
        C_sum = C1 + C2

        m1_dec = C1 % key
        m2_dec = C2 % key
        m_sum_dec = C_sum % key

        st.markdown("**(1) 개별 암호문 생성**")
        st.code(
            f"""
키 K = {key}

평문 m1 = {m1}
랜덤 r1 = {r1}
암호문 C1 = m1 + r1*K = {C1}

평문 m2 = {m2}
랜덤 r2 = {r2}
암호문 C2 = m2 + r2*K = {C2}
""",
            language="text",
        )

        st.markdown("**(2) 서버에서 하는 일 (암호문끼리 덧셈만 수행)**")
        st.code(
            f"""
서버는 평문을 모른 채로, 암호문들만 더합니다.

C_sum = C1 + C2 = {C_sum}
""",
            language="text",
        )

        st.markdown("**(3) 복호화: C mod K**")
        st.code(
            f"""
복호화(예시):

C1 mod K = {C1} mod {key} = {m1_dec}   (원래 m1 = {m1})
C2 mod K = {C2} mod {key} = {m2_dec}   (원래 m2 = {m2})

C_sum mod K = {C_sum} mod {key} = {m_sum_dec}
원래 m1 + m2 = {m1} + {m2} = {m1 + m2}
""",
            language="text",
        )

        if m1 + m2 == m_sum_dec:
            st.success("✅ 암호 상태에서 더한 뒤 복호화해도, 평문 덧셈 결과와 정확히 일치합니다!")
        else:
            st.warning(
                "⚠ m1 + m2 ≥ K 이라서, 이 단순한 장난감 예시에서는 결과가 정확히 일치하지 않을 수 있습니다.\n"
                "→ K 값을 더 크게 설정해 보세요."
            )

        st.info(
            "이 예시는 보안적으로 안전한 실제 동형암호가 아니라, "
            "‘암호 상태에서 연산이 가능하다’는 개념을 수학적으로 맛보는 교육용 장난감 모델입니다.\n"
            "실제 FHE(Fully Homomorphic Encryption)는 훨씬 복잡한 수학과 큰 수 연산을 사용합니다."
        )
    else:
        st.caption("버튼을 눌러 암호화·복호화 과정을 단계별로 확인해 보세요.")
    st.markdown("</div>", unsafe_allow_html=True)
