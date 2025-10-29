import streamlit as st
import random

# ---------------------------
# 기본 설정
# ---------------------------
st.set_page_config(page_title="감정 기반 플레이리스트 🎧", page_icon="🎵", layout="centered")

st.title("🎧 감정 기반 플레이리스트 생성기 (무료 버전)")
st.write("지금 당신의 **감정**과 듣고 싶은 **장르**를 알려주세요. 맞춤 플레이리스트를 만들어드릴게요!")

# ---------------------------
# 사용자 입력
# ---------------------------
emotion = st.text_input("💭 지금 당신의 감정은 어떤가요?", placeholder="예: 설레, 우울해, 행복해, 피곤해...")
genre = st.selectbox("🎶 듣고 싶은 장르는?", ["팝", "힙합", "발라드", "락", "R&B", "재즈", "EDM"])

# ---------------------------
# 랜덤 플레이리스트 생성 함수
# ---------------------------
def generate_playlist(emotion, genre):
    playlist_titles = [
        f"{emotion}할 때 듣는 {genre} 모음집",
        f"{emotion}한 하루, {genre}로 채우기",
        f"{emotion}의 멜로디 - {genre}",
        f"{genre}로 느끼는 {emotion} Mood"
    ]
    title = random.choice(playlist_titles)

    sample_songs = {
        "팝": ["As It Was - Harry Styles", "Levitating - Dua Lipa", "Anti-Hero - Taylor Swift", "Shivers - Ed Sheeran", "Vampire - Olivia Rodrigo"],
        "힙합": ["Snooze - SZA", "Lose Yourself - Eminem", "DNA - BTS", "God's Plan - Drake", "All of the Lights - Kanye West"],
        "발라드": ["취중고백 - 김민석", "너를 만나 - 폴킴", "Love Poem - 아이유", "그대라는 사치 - 한동근", "그날들 - 이선희"],
        "락": ["Smells Like Teen Spirit - Nirvana", "Counting Stars - OneRepublic", "In the End - Linkin Park", "Yellow - Coldplay", "Boulevard of Broken Dreams - Green Day"],
        "R&B": ["Peaches - Justin Bieber", "Call Out My Name - The Weeknd", "On & On - Erykah Badu", "Location - Khalid", "Get You - Daniel Caesar"],
        "재즈": ["Fly Me To The Moon - Frank Sinatra", "Take Five - Dave Brubeck", "Blue in Green - Miles Davis", "Autumn Leaves - Chet Baker", "So What - Miles Davis"],
        "EDM": ["Titanium - David Guetta", "Animals - Martin Garrix", "Don't You Worry Child - Swedish House Mafia", "Closer - The Chainsmokers", "Wake Me Up - Avicii"]
    }

    songs = random.sample(sample_songs.get(genre, []), 3)

    return title, songs

# ---------------------------
# 실행 버튼
# ---------------------------
if st.button("🎵 플레이리스트 생성하기"):
    if not emotion.strip():
        st.warning("감정을 입력해주세요!")
    else:
        with st.spinner("당신만의 플레이리스트를 만드는 중이에요... 🎶"):
            title, songs = generate_playlist(emotion, genre)
        
        st.subheader(f"📀 {title}")
        st.write("**추천 곡 리스트:**")
        for i, song in enumerate(songs, start=1):
            st.write(f"{i}. {song}")

        # Unsplash 이미지 자동 생성
        image_url = f"https://source.unsplash.com/512x512/?{emotion},{genre},music,album"
        st.image(image_url, caption="🎨 자동 생성된 플레이리스트 표지")

        st.success("완성됐어요! 즐겁게 감상하세요 🎧")

# ---------------------------
# 하단 크레딧
# ---------------------------
st.markdown("---")
st.caption("© 2025 Made with ❤️ by Yoojin using Streamlit")
