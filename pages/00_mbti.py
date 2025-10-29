import streamlit as st
import random
import urllib.parse

# ---------------------------
# 기본 설정
# ---------------------------
st.set_page_config(page_title="감정 기반 플레이리스트 🎧", page_icon="🎵", layout="centered")

# ---------------------------
# 스타일 (네온 다크 테마)
# ---------------------------
st.markdown("""
<style>
body {
    background-color: #0d0d0d;
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
<p style='text-align:center; color:gray;'>감정, 날씨, 장르에 어울리는 음악을 추천해드릴게요 🌙</p>
""", unsafe_allow_html=True)

# ---------------------------
# 사용자 입력
# ---------------------------
emotion = st.text_input("💭 지금 당신의 감정은 어떤가요?", placeholder="예: 설레, 우울해, 행복해, 피곤해...")
weather = st.selectbox("🌤️ 지금 날씨는 어떤가요?", ["맑음", "흐림", "비", "눈", "바람"])
genre = st.selectbox("🎶 듣고 싶은 장르는?", ["팝", "힙합", "K-POP", "락", "R&B", "재즈", "EDM"])

# ---------------------------
# YouTube 검색 링크 함수
# ---------------------------
def youtube_search_link(song_title):
    query = urllib.parse.quote(song_title)
    return f"https://www.youtube.com/results?search_query={query}"

# ---------------------------
# 플레이리스트 생성 함수
# ---------------------------
def generate_playlist(emotion, weather, genre):
    title_templates = [
        f"{emotion}한 {weather}날의 {genre} 플레이리스트",
        f"{weather} 날씨에 어울리는 {emotion}한 {genre} 감성",
        f"{emotion}을 담은 {weather}날의 {genre} 선율",
        f"{weather} 속 {emotion}의 {genre} Vibes"
    ]
    title = random.choice(title_templates)

    # 장르별 노래 후보
    song_pool = {
        "팝": [
            ("As It Was - Harry Styles", "가볍게 흥얼거리며 들을 수 있는 팝 명곡이에요."),
            ("Levitating - Dua Lipa", "밝은 리듬으로 기분을 업시켜주는 노래예요."),
            ("Vampire - Olivia Rodrigo", "감정의 기복을 세련되게 표현한 감성 팝."),
            ("Shivers - Ed Sheeran", "설레는 마음을 담은 팝송이에요."),
            ("Flowers - Miley Cyrus", "스스로를 사랑하자는 메시지를 담은 노래예요.")
        ],
        "힙합": [
            ("Snooze - SZA", "감각적인 힙합과 R&B의 완벽한 조화."),
            ("Lose Yourself - Eminem", "도전과 열정의 상징적인 곡이에요."),
            ("God's Plan - Drake", "긍정적인 에너지를 전해주는 힙합 곡."),
            ("DNA - BTS", "자신감을 폭발시키는 강렬한 비트."),
            ("HUMBLE - Kendrick Lamar", "자기 반성의 메시지를 담은 명곡이에요.")
        ],
        "K-POP": [
            ("Love Dive - IVE", "자신감 넘치는 사랑의 에너지를 담은 곡이에요."),
            ("ETA - NewJeans", "청량한 리듬과 중독성 있는 후렴이 매력적이에요."),
            ("Super Shy - NewJeans", "수줍은 마음을 귀엽게 표현한 곡."),
            ("Super - SEVENTEEN", "에너지 넘치는 퍼포먼스로 기분을 끌어올려줘요."),
            ("ANTIFRAGILE - LE SSERAFIM", "역경을 이겨내는 강인함을 담은 곡이에요."),
            ("Tomboy - (G)I-DLE", "당당하고 솔직한 태도를 표현한 걸크러시 명곡."),
            ("Next Level - aespa", "중독성 강한 비트와 자신감 넘치는 메시지의 곡."),
            ("Love Shot - EXO", "치명적인 분위기와 매혹적인 사운드가 특징이에요."),
            ("I Am - IVE", "스스로의 정체성을 당당히 드러내는 K-POP 명곡."),
            ("Hype Boy - NewJeans", "사랑에 빠진 설렘을 트렌디하게 담아낸 곡이에요.")
        ],
        "락": [
            ("Counting Stars - OneRepublic", "리듬감 넘치고 희망적인 메시지를 담은 록송."),
            ("Smells Like Teen Spirit - Nirvana", "전설적인 록 사운드의 대표작."),
            ("Yellow - Coldplay", "사랑과 따뜻함을 담은 감성 록."),
            ("Boulevard of Broken Dreams - Green Day", "외로움 속에서도 자신을 찾는 노래."),
            ("Paradise - Coldplay", "현실의 벽을 넘어 꿈을 그리는 노래예요.")
        ],
        "R&B": [
            ("Peaches - Justin Bieber", "따뜻한 분위기의 R&B 대표곡이에요."),
            ("Call Out My Name - The Weeknd", "아련한 감정을 세련되게 표현한 곡."),
            ("Get You - Daniel Caesar", "사랑에 빠진 순간을 그린 달콤한 노래."),
            ("Location - Khalid", "감정과 공간이 교차하는 독특한 분위기."),
            ("Under the Influence - Chris Brown", "몽환적인 분위기의 R&B 트랙.")
        ],
        "재즈": [
            ("Fly Me To The Moon - Frank Sinatra", "고전 재즈의 낭만을 느낄 수 있는 곡."),
            ("Take Five - Dave Brubeck", "재즈의 리듬을 대표하는 명곡이에요."),
            ("Autumn Leaves - Chet Baker", "가을 감성에 딱 어울리는 잔잔한 재즈."),
            ("Blue in Green - Miles Davis", "서정적인 감정선이 돋보이는 곡."),
            ("My Funny Valentine - Chet Baker", "부드럽고 감미로운 발렌타인데이의 정서.")
        ],
        "EDM": [
            ("Animals - Martin Garrix", "폭발적인 에너지의 EDM 대표곡."),
            ("Titanium - David Guetta", "자신감을 높여주는 강렬한 곡이에요."),
            ("Closer - The Chainsmokers", "로맨틱하면서도 신나는 EDM."),
            ("Wake Me Up - Avicii", "희망찬 감정을 담은 EDM 명곡."),
            ("Don't You Worry Child - Swedish House Mafia", "감동적인 멜로디가 인상적인 곡이에요.")
        ]
    }

    selected = random.sample(song_pool.get(genre, []), 5)
    playlist = []
    for title_text, desc in selected:
        playlist.append({
            "title": title_text,
            "desc": desc,
            "url": youtube_search_link(title_text)
        })
    return title, playlist

# ---------------------------
# 실행 버튼
# ---------------------------
if st.button("🎵 플레이리스트 생성하기"):
    if not emotion.strip():
        st.warning("감정을 입력해주세요!")
    else:
        with st.spinner("감정에 맞는 노래를 찾는 중이에요... 🎶"):
            title, playlist = generate_playlist(emotion, weather, genre)

        cover_url = f"https://source.unsplash.com/800x600/?{emotion},{weather},{genre},music,album"

        st.markdown(f"""
        <div style="text-align:center; margin-top:30px;">
            <img src="{cover_url}" width="70%" style="border-radius:20px; box-shadow:0 0 25px rgba(29,185,84,0.5);">
            <h2 style="margin-top:20px;">{title}</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        for song in playlist:
            st.markdown(f"""
            <div class="playlist-card">
                <h4>{song['title']}</h4>
                <p style="color:#ccc;">{song['desc']}</p>
                <a href="{song['url']}" target="_blank">▶ YouTube에서 듣기</a>
            </div>
            """, unsafe_allow_html=True)

        st.success("✨ 당신만의 감성 플레이리스트가 완성됐어요! 🎧")

# ---------------------------
# 하단
# ---------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("© 2025 Made with 💚 by Yoojin | 감정·날씨·장르 기반 음악 큐레이터 🎶")


