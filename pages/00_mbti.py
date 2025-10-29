import streamlit as st
from youtubesearchpython import VideosSearch
import random

# ---------------------------
# 기본 설정
# ---------------------------
st.set_page_config(page_title="감정 기반 플레이리스트 🎧", page_icon="🎵", layout="centered")

# 다크 테마 스타일
st.markdown("""
<style>
body {
    background-color: #0e0e0e;
    color: white;
    font-family: 'Pretendard', sans-serif;
}
h1, h2, h4 {
    color: #1DB954;
}
.playlist-card {
    background-color: #1a1a1a;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0 0 10px rgba(29,185,84,0.4);
    transition: 0.3s;
}
.playlist-card:hover {
    box-shadow: 0 0 20px rgba(29,185,84,0.7);
    transform: translateY(-2px);
}
a {
    color: #1DB954;
    text-decoration: none;
    font-weight: bold;
}
a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# 헤더
# ---------------------------
st.markdown("""
<h1 style='text-align:center;'>🎧 감정 기반 플레이리스트 생성기</h1>
<p style='text-align:center; color:gray;'>당신의 감정, 날씨, 그리고 원하는 장르에 어울리는 진짜 노래를 추천해드릴게요 🌙</p>
""", unsafe_allow_html=True)

# ---------------------------
# 사용자 입력
# ---------------------------
emotion = st.text_input("💭 지금 당신의 감정은 어떤가요?", placeholder="예: 설레, 우울해, 행복해, 피곤해...")
weather = st.selectbox("🌤️ 지금 날씨는 어떤가요?", ["맑음", "흐림", "비", "눈", "바람"])
genre = st.selectbox("🎶 듣고 싶은 장르는?", ["팝", "힙합", "발라드", "락", "R&B", "재즈", "EDM"])

# ---------------------------
# YouTube 검색 함수
# ---------------------------
def get_youtube_link(song_name):
    try:
        search = VideosSearch(song_name, limit=1)
        result = search.result()
        if result["result"]:
            return result["result"][0]["link"]
    except:
        return None

# ---------------------------
# 플레이리스트 생성
# ---------------------------
def generate_playlist(emotion, weather, genre):
    title_templates = [
        f"{emotion}한 {weather}날의 {genre} 플레이리스트",
        f"{weather} 날씨에 어울리는 {emotion}한 {genre} 감성",
        f"{emotion}을 담은 {weather}날의 {genre} 선율",
        f"{weather} 속 {emotion}의 {genre} Vibes"
    ]
    title = random.choice(title_templates)

    # 곡 리스트 (간단한 장르 기반)
    song_pool = {
        "팝": ["As It Was - Harry Styles", "Levitating - Dua Lipa", "Vampire - Olivia Rodrigo", "Shivers - Ed Sheeran", "Flowers - Miley Cyrus"],
        "힙합": ["Snooze - SZA", "Lose Yourself - Eminem", "God's Plan - Drake", "DNA - BTS", "HUMBLE - Kendrick Lamar"],
        "발라드": ["너를 만나 - 폴킴", "Love Poem - 아이유", "취중고백 - 김민석", "그대라는 사치 - 한동근", "너무 보고 싶어 - 김범수"],
        "락": ["Counting Stars - OneRepublic", "Smells Like Teen Spirit - Nirvana", "Yellow - Coldplay", "Boulevard of Broken Dreams - Green Day", "Paradise - Coldplay"],
        "R&B": ["Peaches - Justin Bieber", "Call Out My Name - The Weeknd", "Get You - Daniel Caesar", "Location - Khalid", "Under the Influence - Chris Brown"],
        "재즈": ["Fly Me To The Moon - Frank Sinatra", "Take Five - Dave Brubeck", "Autumn Leaves - Chet Baker", "Blue in Green - Miles Davis", "My Funny Valentine - Chet Baker"],
        "EDM": ["Animals - Martin Garrix", "Titanium - David Guetta", "Closer - The Chainsmokers", "Wake Me Up - Avicii", "Don't You Worry Child - Swedish House Mafia"]
    }

    songs = random.sample(song_pool.get(genre, []), 5)
    playlist = []
    for song in songs:
        url = get_youtube_link(song)
        playlist.append({
            "title": song,
            "desc": f"'{emotion}'한 {weather}날에 어울리는 {genre} 느낌의 곡입니다.",
            "url": url or "https://www.youtube.com"
        })

    return title, playlist

# ---------------------------
# 실행
# ---------------------------
if st.button("🎵 플레이리스트 생성하기"):
    if not emotion.strip():
        st.warning("감정을 입력해주세요!")
    else:
        with st.spinner("감정에 맞는 노래를 찾는 중이에요... 🎶"):
            title, playlist = generate_playlist(emotion, weather, genre)

        cover_url = f"https://source.unsplash.com/800x600/?{emotion},{weather},{genre},music,album"

        # 표지 및 제목
        st.markdown(f"""
        <div style="text-align:center; margin-top:30px;">
            <img src="{cover_url}" width="70%" style="border-radius:20px; box-shadow:0 0 25px rgba(29,185,84,0.5);">
            <h2 style="margin-top:20px;">{title}</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 노래 카드
        for song in playlist:
            st.markdown(f"""
            <div class="playlist-card">
                <h4>{song['title']}</h4>
                <p style="color: #ccc;">{song['desc']}</p>
                <a href="{song['url']}" target="_blank">▶ YouTube에서 듣기</a>
            </div>
            """, unsafe_allow_html=True)

        st.success("✨ 당신만의 감성 플레이리스트가 완성됐어요! 🎧")

# ---------------------------
# 크레딧
# ---------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("© 2025 Made with 💚 by Yoojin | 감정·날씨·장르 기반 음악 추천기 🎶")

