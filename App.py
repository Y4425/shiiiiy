import streamlit as st
import pandas as pd
import hashlib
import random

# -------------------------------------------------
# 기본 설정 & 공통 스타일
# -------------------------------------------------
st.set_page_config(
    page_title="데이터 가명처리 · 익명처리 · 동형암호 학습 앱",
    layout="centered"
)

GLOBAL_CSS = """
<style>
body {
    background-color: #F4F5FB;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
}
.card {
    background: #FFFFFF;
    padding: 18px 20px;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08);
    margin-top: 10px;
    margin-bottom: 10px;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 800;
    color: #283593;
    margin-bottom: 0.3rem;
}
.sub-caption {
    font-size: 0.9rem;
    color: #555555;
}
.label-chip {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    background: #E8EAF6;
    color: #283593;
    font-size: 0.8rem;
    font-weight: 600;
}
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
.stButton > button {
    background: linear-gradient(90deg, #5C6BC0, #3949AB);
    color: white;
    border-radius: 999px;
    padding: 0.5rem 1.4rem;
    border: none;
    font-weight: 600;
}
code {
    font-size: 0.8rem !important;
}
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# -------------------------------------------------
# 상단 타이틀 + 전체 학습 가이드
# -------------------------------------------------
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

st.markdown(
    """
    <div style="text-align:center; margin-bottom: 1.2rem;">
        <div style="font-size:2.0rem; font-weight:800; color:#283593;">
            🧬 데이터 가명처리 · 익명처리 · 동형암호 학습 앱
        </div>
        <div style="margin-top:0.4rem; font-size:0.95rem; color:#555;">
            개인정보 보호 기술(가명처리, 익명화, 동형암호 개념)을
            <b>직접 실험</b>해 보며 배우는 교육용 웹앱입니다.
        </div>
        <div style="margin-top:0.3rem;">
            <span class="label-chip">가명처리</span>
            <span class="label-chip">익명·비식별화</span>
            <span class="label-chip">동형암호</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("📘 이 앱을 어떻게 사용하면 좋을까? (학습 가이드)", expanded=True):
    st.markdown(
        """
        **추천 학습 순서**

        1️⃣ 1탭(가명처리)에서 *해시와 마스킹* 개념을 눈으로 확인  
        2️⃣ 2탭(익명·비식별화)에서 *k-익명성*과 이상치, 일반화를 체험  
        3️⃣ 3탭(동형암호)에서 *평문·암호문·복호화* 관계를 수식으로 이해  

        각 탭에는  
        - **학습 목표**  
        - **개념 정리**  
        - **실습 단계 안내**  
        - **미니 퀴즈**  

        가 들어 있어서,  
        그냥 위에서부터 **천천히 따라 하기만 해도** 개념이 어느 정도 잡히도록 구성했습니다.
        """
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
        <b>학습 목표</b><br>
        · 가명처리가 무엇인지 말로 설명할 수 있다.<br>
        · 해시(hash)와 마스킹(masking)의 차이를 이해한다.<br>
        · 같은 주민번호라도 salt가 다르면 다른 가명 ID가 만들어짐을 확인한다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("📚 개념 정리: 가명처리 · 해시 · salt", expanded=False):
        st.markdown(
            """
            - **가명처리**: 이름, 주민번호처럼 직접 개인을 식별할 수 있는 값을 다른 값으로 치환해 두는 것  
            - **마스킹**: 일부 글자를 `*` 등으로 가려서 원래 값을 바로 보이지 않게 만드는 것  
            - **해시(Hash)**: 입력값을 고정 길이의 '되돌릴 수 없는' 문자열로 바꾸는 함수  
            - **Salt**: 같은 값이라도 다른 해시가 나오도록 섞어 넣는 추가 문자열<br>
              (원래 값 + salt → 해시 → 가명 ID)
            """
        )

    # 입력 영역
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**① 원본 개인정보 입력**")
        name = st.text_input("이름", value="홍길동")
        rrn = st.text_input("주민번호(예시)", value="000101-3123456")
        phone = st.text_input("전화번호(예시)", value="010-1234-5678")
        st.caption("※ 실제 주민번호/전화번호 대신 예시 데이터를 사용하는 것이 좋습니다.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**② 가명 ID 생성을 위한 비밀키(salt)**")
        salt = st.text_input("비밀키(salt)", value="my_secret_key")
        st.caption("같은 주민번호라도 salt를 바꾸면 다른 가명 ID가 생성됩니다.")
        st.markdown("</div>", unsafe_allow_html=True)

    # 함수 정의
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

    def make_pseudo_id(text: str, salt_value: str = "") -> str:
        base = (text + salt_value).encode("utf-8")
        return hashlib.sha256(base).hexdigest()

    # 실행 영역
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**③ 가명처리 실행**")

    if st.button("🔐 가명처리 결과 보기"):
        masked_name = mask_name(name)
        masked_rrn = mask_rrn(rrn)
        masked_phone = mask_phone(phone)
        pseudo_id = make_pseudo_id(rrn + phone, salt)

        result_df = pd.DataFrame(
            {
                "항목": ["이름", "주민번호", "전화번호", "가명 ID(해시)"],
                "원본 값": [name, rrn, phone, "(원본을 직접 저장하지 않음)"],
                "가명/마스킹 결과": [
                    masked_name,
                    masked_rrn,
                    masked_phone,
                    pseudo_id[:16] + "...",
                ],
            }
        )

        st.dataframe(result_df, use_container_width=True)
        st.info(
            "실제 시스템에서는 주민번호·전화번호 대신 이런 가명 ID만 저장하여 "
            "데이터가 유출되어도 원래 사람을 바로 알아보기 어렵게 만듭니다."
        )
    else:
        st.caption("버튼을 눌러 가명처리 결과를 확인해 보세요.")
    st.markdown("</div>", unsafe_allow_html=True)

    # 미니 퀴즈
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**🧩 미니 퀴즈: 해시와 가명처리 이해 점검**")
    q1 = st.radio(
        "Q1. 해시(hash) 값만으로는 원래 주민번호를 다시 알아낼 수 있다.",
        ["그렇다", "아니다"],
        index=1,
    )
    if q1 == "그렇다":
        st.error("❌ 해시는 되돌릴 수 없는 일방향 함수라 복호화가 불가능합니다.")
    else:
        st.success("✅ 정답! 해시는 평문으로 복호화할 수 없기 때문에 가명처리에 적합합니다.")

    q2 = st.radio(
        "Q2. salt를 바꾸면 같은 주민번호라도 다른 가명 ID가 나오는 이유는?",
        [
            "랜덤하게 바뀌어서",
            "해시 입력값 자체가 달라지기 때문",
            "주민번호가 바뀌기 때문",
        ],
        index=1,
    )
    if q2 == "해시 입력값 자체가 달라지기 때문":
        st.success("✅ 정확합니다! (주민번호 + salt)가 해시의 입력이기 때문에 입력이 바뀌면 결과도 달라집니다.")
    else:
        st.info("ℹ️ 해시 함수는 입력이 조금만 달라도 완전히 다른 결과를 내는 성질을 갖고 있습니다.")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# 2. 익명·비식별화 탭
# -------------------------------------------------
with tab2:
    st.markdown('<div class="section-title">2️⃣ 익명·비식별화 (k-Anonymity)</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="sub-caption">
        <b>학습 목표</b><br>
        · 익명·비식별화와 가명처리의 차이를 설명할 수 있다.<br>
        · k-익명성에서 k의 의미를 이해한다.<br>
        · 나이 구간과 우편번호 자릿수 조정이 k 값에 미치는 영향을 관찰한다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("📚 개념 정리: 익명처리 · k-익명성", expanded=False):
        st.markdown(
            """
            - **익명·비식별화**: 개별 인물을 특정하기 어렵도록 정보(나이, 주소 등)를 일반화하거나 제거하는 것  
            - **준식별자**: 단독으로는 애매하지만, 몇 개 조합하면 개인을 추론할 수 있는 정보 (나이, 성별, 우편번호 등)  
            - **k-익명성**: 어떤 속성 조합에 속한 사람이 최소 k명 이상이면, 그 중 누가 누구인지 알아보기 어려운 상태  
            """
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
    st.markdown("**① 원본 데이터 (작은 의료 데이터 예시)**")
    st.dataframe(raw_data, use_container_width=True)
    st.caption("※ 실제 의료 데이터는 훨씬 더 크고, 더 많은 속성을 포함합니다.")
    st.markdown("</div>", unsafe_allow_html=True)

    # 설정
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**② 익명화 설정 (나이 구간 · 우편번호 자릿수)**")
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
    st.caption("※ 나이 구간을 넓게 하고 우편번호 자릿수를 줄일수록 그룹이 커지고 k 값이 커지는 경향이 있습니다.")
    st.markdown("</div>", unsafe_allow_html=True)

    # 일반화 함수
    def generalize_age(age: int, group_size: int) -> str:
        base = (age // group_size) * group_size
        return f"{base}~{base + group_size - 1}"

    def generalize_zip(zipcode: str, keep: int) -> str:
        if len(zipcode) <= keep:
            return zipcode
        return zipcode[:keep] + "*" * (len(zipcode) - keep)

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

    # k가 작으면 자동 보정
    target_k = 3
    auto_adjusted = False
    if min_k < target_k:
        auto_adjusted = True
        age_group_size = max(age_group_size, 15)
        zip_keep = min(zip_keep, 2)
        anon_df["나이_구간"] = anon_df["나이"].apply(lambda x: generalize_age(x, age_group_size))
        anon_df["우편번호_일반화"] = anon_df["우편번호"].apply(lambda x: generalize_zip(x, zip_keep))
        group_k = (
            anon_df.groupby(group_cols)
            .size()
            .reset_index(name="k")
            .sort_values("k", ascending=False)
        )
        min_k = int(group_k["k"].min())

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**③ 익명화(일반화) 결과 – 그룹별 k 값**")

    if auto_adjusted:
        st.warning(
            f"초기 설정에서 일부 그룹의 k 값이 {target_k} 미만이라, 자동으로 나이 구간과 우편번호 자릿수를 조정했습니다.\n"
            f"→ 현재 기준: 나이 {age_group_size}살 단위, 우편번호 앞 {zip_keep}자리"
        )

    for _, row in group_k.iterrows():
        k_val = int(row["k"])
        age_r = row["나이_구간"]
        zip_r = row["우편번호_일반화"]

        if k_val < 3:
            badge = f"<span class='k-badge-small'>k={k_val}</span>"
        elif k_val < 5:
            badge = f"<span class='k-badge-mid'>k={k_val}</span>"
        else:
            badge = f"<span class='k-badge-good'>k={k_val}</span>"

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
    with st.expander("📊 익명화된 상세 데이터 테이블"):
        st.dataframe(
            anon_df[["나이_구간", "우편번호_일반화", "질병"]],
            use_container_width=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # 미니 퀴즈
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**🧩 미니 퀴즈: k-익명성 이해 점검**")
    q3 = st.radio(
        "Q1. 어떤 그룹의 k 값이 1이면, 이 그룹에 속한 사람은 어떻게 될까?",
        [
            "다른 사람들과 섞여서 안전하다.",
            "해당 사람을 다시 식별할 위험이 크다.",
            "k 값과는 상관없다.",
        ],
        index=1,
    )
    if q3 == "해당 사람을 다시 식별할 위험이 크다.":
        st.success("✅ 정답! k=1이면 사실상 개인 하나만 구분되므로 재식별 위험이 매우 큽니다.")
    else:
        st.info("ℹ️ k 값이 작을수록(1에 가까울수록) '누군지 특정될 가능성'이 커진다는 점이 핵심입니다.")

    q4 = st.radio(
        "Q2. k 값을 키우고 싶다면 어떻게 해야 할까?",
        [
            "나이 구간을 더 잘게 나눈다.",
            "우편번호를 더 길게 표시한다.",
            "나이 구간을 넓히거나 우편번호 자릿수를 줄인다.",
        ],
        index=2,
    )
    if q4 == "나이 구간을 넓히거나 우편번호 자릿수를 줄인다.":
        st.success("✅ 맞아요! 일반화를 강하게 할수록 더 많은 사람이 같은 그룹에 묶여 k가 커집니다.")
    else:
        st.info("ℹ️ 세부 정보가 많을수록 개인을 더 쉽게 구분할 수 있다는 점을 떠올려 보세요.")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# 3. 동형암호(개념 실습) 탭
# -------------------------------------------------
with tab3:
    st.markdown('<div class="section-title">3️⃣ 동형암호 개념 실습 (장난감 예시)</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="sub-caption">
        <b>학습 목표</b><br>
        · 평문, 암호문, 복호화, 키의 의미를 구분할 수 있다.<br>
        · 장난감 동형암호 모형을 통해 '암호 상태로 연산' 개념을 이해한다.<br>
        · 왜 m1 + m2와 (C1 + C2) mod K가 같아지는지 수식으로 설명할 수 있다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("📚 개념 정리: 평문 · 암호문 · 복호화 · 키", expanded=False):
        st.markdown(
            """
            - **평문(Plaintext)**: 암호화되기 전의 원래 데이터 (예: 5, 7 같은 숫자)  
            - **암호문(Ciphertext)**: 평문을 숨겨 놓은 데이터. 겉으로 보기에는 의미 없는 수/문자열  
            - **키(Key)**: 암호를 만들거나 풀 때 사용하는 비밀 값  
            - **복호화(Decryption)**: 암호문과 키를 이용해 다시 평문으로 되돌리는 과정  
            """
        )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**① 키와 평문 값 설정**")

    key = st.slider("암호 키 K (충분히 큰 정수)", min_value=50, max_value=300, value=101, step=1)
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        m1 = st.number_input("첫 번째 평문 값 m1", min_value=0, max_value=20, value=5, step=1)
    with col_m2:
        m2 = st.number_input("두 번째 평문 값 m2", min_value=0, max_value=20, value=7, step=1)

    st.caption("※ 조건: m1 + m2 < K 범위 안에 있을수록 결과가 더 잘 맞습니다.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**② 암호화 · 연산 · 복호화 과정 보기**")

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

        st.markdown("**(3) 복호화: C mod K 계산**")
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

    # 미니 퀴즈
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**🧩 미니 퀴즈: 동형암호 개념 점검**")

    q5 = st.radio(
        "Q1. 서버는 어떤 정보를 모른 채로 계산을 수행하는가?",
        ["평문 값(m1, m2)", "키 K", "암호문 C1, C2"],
        index=0,
    )
    if q5 == "평문 값(m1, m2)":
        st.success("✅ 맞아요! 서버는 평문을 몰라도 암호문끼리 연산만 수행합니다.")
    else:
        st.info("ℹ️ 동형암호의 핵심은 '평문을 알 필요 없이 암호문만 가지고 계산 가능'이라는 점입니다.")

    q6 = st.radio(
        "Q2. 이 장난감 예시에서 복호화에 사용되는 연산은?",
        ["덧셈", "나눗셈", "mod K 연산"],
        index=2,
    )
    if q6 == "mod K 연산":
        st.success("✅ 정답! C = m + rK 이므로 C mod K = m 이 되어 평문을 되찾을 수 있습니다.")
    else:
        st.info("ℹ️ C = m + rK 에서 K의 배수 부분은 mod K를 하면 0이 된다는 점을 떠올려 보세요.")
    st.markdown("</div>", unsafe_allow_html=True)
