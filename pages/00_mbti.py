import streamlit as st
import random
from PIL import Image
import io
import openai

# ---------------------------
# 기본 설정
# ---------------------------
st.set_page_config(page_title="감정 기반 플레이리스트 🎧", page_icon="🎵", layout="centered")

st.title("🎧 감정 기반 플레이리스트 생성기")
st.write("지금 당신의 감정과 듣고 싶은 장르를 알려주세요. 맞춤 플레이리스트를 만들어드릴게요!")

# ---------------------------
# 사용자 입력
# ---------------------------
emotion = st.text_input("💭 지금 당신의 감정은 어떤가요?", placeholder="예: 행복해, 우울해, 설레, 피곤해...")
genre = st.selectbox("🎶 듣고 싶은 장르는?", ["팝", "힙합", "발라드", "락", "R&B", "재즈", "EDM", "기타"])

# ---------------------------
# AI 응답 생성 함수 (모의 추천)
# ---------------------------
def generate_playlist(emotion, genre):
    playlist_names = [
        f"{emotion} {genre} Mood",
        f"{emotion}할 때 듣는 {genre}",
        f"{emotion} Vibes in {genre}",
        f"{emotion}한 하루를 위한 {genre} 플레이리스트"
    ]
    playlist_title = random.choice(playlist_names)

    # 샘플 노래 데이터 (원한다면 Spotify API로 연결 가능)
    sample_songs = {
        "팝": ["As It Was - Harry Styles", "Levitating - Dua Lipa", "Anti-Hero - Taylor Swift"],
        "힙합": ["Snooze - SZA", "Industry Baby - Lil Nas X", "Lose Yourself - Eminem"],
        "발라드": ["취중고백 - 김민석", "너를 만나 - 폴킴", "Love Poem - 아이유"],
        "락": ["Smells Like Teen Spirit - Nirvana", "Counting Stars - OneRepublic", "In the End - Linkin Park"],
        "R&B": ["Peaches - Justin Bieber", "Call Out My Name - The Weeknd", "On & On - Erykah Badu"],
        "재즈": ["Fly Me To The Moon - Frank Sinatra", "Take Five - Dave Brubeck", "Blue in Green - Miles Davis"],
        "EDM": ["Titanium - David Guetta", "Animals - Martin Garrix", "Don't You Worry Child - Swedish House Mafia"],
        "기타": ["Random Song 1", "Random Song 2", "Random Song 3"]
    }

    playlist_songs = random.sample(sample_songs.get(genre, []), k=3)
    return playlist_title, playlist_songs

# ---------------------------
# 표지 이미지 생성 (OpenAI 이미지 API 사용 예시)
# ---------------------------
def generate_cover_image(emotion, genre):
    prompt = f"{emotion}한 분위기의 {genre} 플레이리스트 앨범 커버, 감성적이고 예술적인 스타일"
    image_bytes = openai.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="512x512"
    ).data[0].b64_json
    image = Image.open(io.BytesIO(base64.b64decode(image_bytes)))
    return image

# ---------------------------
# 결과 출력
# ---------------------------
if st.button("🎵 플레이리스트 생성하기"):
    if emotion.strip() == "":
        st.warning("감정을 입력해주세요!")
    else:
        title, songs = generate_playlist(emotion, genre)

        st.subheader(f"📀 {title}")
        st.write("**추천 곡 리스트:**")
        for i, song in enumerate(songs, start=1):
            st.write(f"{i}. {song}")

        # 이미지 (OpenAI 이미지 생성 대신 예시 이미지 사용 가능)
        st.image("https://source.unsplash.com/512x512/?music,album," + genre, caption="🎨 자동 생성된 플레이리스트 표지")

        st.success("플레이리스트가 완성되었어요! 🎶")

---

### 🚀 실행 방법
1. 파일 이름을 예: `playlist_app.py` 로 저장  
2. 터미널에서 실행  
   ```bash
   streamlit run playlist_app.py
