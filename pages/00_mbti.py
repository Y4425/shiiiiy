import streamlit as st
import openai
import base64
from PIL import Image
import io

# ---------------------------
# 기본 설정
# ---------------------------
st.set_page_config(page_title="감정 기반 플레이리스트 🎧", page_icon="🎵", layout="centered")

st.title("🎧 감정 기반 플레이리스트 생성기")
st.write("지금 당신의 **감정**과 듣고 싶은 **장르**를 알려주세요. 맞춤 플레이리스트를 만들어드릴게요!")

# ---------------------------
# API Key 입력 (streamlit.io에서 Secrets에 저장!)
# ---------------------------
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ---------------------------
# 사용자 입력
# ---------------------------
emotion = st.text_input("💭 지금 당신의 감정은 어떤가요?", placeholder="예: 설레, 우울해, 행복해, 피곤해...")
genre = st.selectbox("🎶 듣고 싶은 장르는?", ["팝", "힙합", "발라드", "락", "R&B", "재즈", "EDM"])

# ---------------------------
# GPT를 이용한 플레이리스트 생성 함수
# ---------------------------
def generate_playlist(emotion, genre):
    prompt = f"""
    사용자의 감정은 '{emotion}', 듣고 싶은 장르는 '{genre}'입니다.
    이 정보를 바탕으로 다음을 만들어주세요:
    1. 감정에 어울리는 플레이리스트 제목 (한 문장)
    2. 추천 곡 5곡 (노래 제목 - 가수 형식)
    3. 전체를 한국어로 감성적으로 표현
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "당신은 감성적인 음악 큐레이터입니다."},
                  {"role": "user", "content": prompt}],
        temperature=0.8
    )
    return response.choices[0].message["content"]

# ---------------------------
# 표지 이미지 생성 함수
# ---------------------------
def generate_cover_image(emotion, genre):
    prompt = f"{emotion}한 분위기의 {genre} 플레이리스트 앨범 커버, 감성적이고 예술적인 스타일, 고해상도"
    result = openai.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="512x512"
    )
    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    image = Image.open(io.BytesIO(image_bytes))
    return image

# ---------------------------
# 실행 버튼
# ---------------------------
if st.button("🎵 플레이리스트 생성하기"):
    if not emotion.strip():
        st.warning("감정을 입력해주세요!")
    else:
        with st.spinner("플레이리스트를 만드는 중이에요... 🎶"):
            playlist_text = generate_playlist(emotion, genre)
            image = generate_cover_image(emotion, genre)

        st.subheader("📀 나만의 감정 플레이리스트")
        st.markdown(playlist_text)
        st.image(image, caption="🎨 자동 생성된 앨범 커버")
        st.success("완성됐어요! 즐겁게 감상하세요 🎧")
