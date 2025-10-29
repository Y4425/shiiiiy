import streamlit as st
import random
import urllib.parse

st.set_page_config(page_title="너를 위한 플레이리스트 💫🎧🎀", page_icon="🎧", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
body {
    background: linear-gradient(135deg, #0d0d0d 20%, #1a001a 90%);
    color: #fce4ec;
    font-family: 'Poppins', sans-serif;
}
h1 {
    text-align: center;
    font-size: 2.8em;
    background: linear-gradient(90deg, #ff8af3, #ff5dc8, #fce4ec);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    text-shadow: 0 0 10px rgba(255,105,180,0.6);
}
p {
    text-align: center;
    color: #d9b3ff;
    font-size: 1em;
}
.playlist-card {
    background: rgba(35, 0, 35, 0.8);
    border: 1px solid rgba(255, 100, 180, 0.3);
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 18px;
    box-shadow: 0 0 20px rgba(255, 90, 200, 0.2);
    transition: 0.3s;
}
.playlist-card:hover {
    box-shadow: 0 0 30px rgba(255, 110, 210, 0.5);
    transform: scale(1.02);
}
h2 {
    color: #ff80c0;
    text-align: center;
    margin-top: 25px;
    text-shadow: 0 0 10px rgba(255, 90, 200, 0.6);
}
h4 {
    color: #ffbdf0;
}
a {
    color: #ff7adf;
    text-decoration: none;
    font-weight: bold;
}
a:hover {
    text-decoration: underline;
    color: #ffc0f0;
}
.stTextInput input {
    background-color: #1a001a;
    color: #fff;
    border-radius: 12px;
    border: 1px solid #ff80c0;
}
.stSelectbox select {
    background-color: #1a001a;
    color: #fff;
    border-radius: 12px;
    border: 1px solid #ff80c0;
}
.stButton>button {
    background: linear-gradient(90deg, #ff80c0, #ff4dc4);
    color: white;
    font-weight: 600;
    border-radius: 12px;
    padding: 10px 25px;
    border: none;
    transition: 0.3s;
    box-shadow: 0 0 15px rgba(255, 80, 180, 0.5);
}
.stButton>button:hover {
    background: linear-gradient(90deg, #ff4dc4, #ff80c0);
    transform: scale(1.05);
    box-shadow: 0 0 25px rgba(255, 120, 200, 0.7);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1>너를 위한 플레이리스트 💫🎧🎀</h1>
<p>감정, 날씨, 그리고 취향으로 완성되는 힙한 나만의 음악 리스트 💋</p>
""", unsafe_allow_html=True)

emotion = st.text_input("💭 지금 기분은 어때?", placeholder="예: 설레, 우울해, 기분 좋아, 피곤해...")
weather = st.selectbox("🌤️ 지금 날씨는 어때?", ["맑음", "흐림", "비", "눈", "바람"])
genre = st.selectbox("🎶 듣고 싶은 장르는?", ["팝", "힙합", "K‑POP", "락", "R&B", "재즈", "EDM"])

def youtube_search_link(song_title):
    query = urllib.parse.quote(song_title)
    return f"https://www.youtube.com/results?search_query={query}"

def generate_playlist(emotion, weather, genre):
    title_templates = [
        f"{emotion}한 {weather}날, 너에게 어울리는 {genre} Mood 💗",
        f"{weather} 속 {emotion} 감성을 담은 {genre} Playlist 💋",
        f"{emotion}한 하루를 위한 {genre} Tracks 💫",
        f"{weather}인 오늘, {emotion}한 {genre} vibes 🎀"
    ]
    title = random.choice(title_templates)

    song_pool = {
        "팝": [
            ("As It Was - Harry Styles", "가볍게 흥얼거리며 들을 수 있는 팝 명곡."),
            ("Levitating - Dua Lipa", "밝은 리듬으로 기분을 업시켜주는 노래."),
            ("Shivers - Ed Sheeran", "설레는 마음을 담은 팝송."),
            ("Vampire - Olivia Rodrigo", "감정의 기복을 세련되게 표현한 감성 팝."),
            ("Flowers - Miley Cyrus", "스스로를 사랑하자는 메시지를 담은 노래.")
        ],
        "힙합": [
            ("Snooze - SZA", "감각적인 힙합과 R&B의 완벽한 조화."),
            ("Lose Yourself - Eminem", "도전과 열정의 상징적인 곡."),
            ("God's Plan - Drake", "긍정적인 에너지를 전해주는 힙합 곡."),
            ("DNA - BTS", "자신감을 폭발시키는 강렬한 비트."),
            ("HUMBLE - Kendrick Lamar", "자기 반성의 메시지를 담은 명곡.")
        ],
        "K‑POP": [
            # 기존 + 추가 실제 있는 남자아이돌 곡들
            ("Love Dive - IVE", "자신감 넘치는 사랑의 에너지를 담은 곡."),
            ("ETA - NewJeans", "청량한 리듬과 중독성 있는 후렴이 매력적이에요."),
            ("Super Shy - NewJeans", "수줍은 마음을 귀엽게 표현한 곡."),
            ("MANIAC - Stray Kids", "틀을 깨고 나아가는 강렬한 퍼포먼스가 돋보이는 곡이에요."),  # 실제 존재함 :contentReference[oaicite:1]{index=1}
            ("Lalalala - Stray Kids", "축하와 자유로움을 담아낸 신나는 노래예요."),  # 실제 존재함 :contentReference[oaicite:2]{index=2}
            ("Wish - NCT WISH", "희망찬 메시지로 데뷔한 그들의 대표 싱글이예요."),  # 실제 존재함 :contentReference[oaicite:3]{index=3}
            ("What You Want - CORTIS", "새로운 보이그룹의 시작을 알리는 데뷔곡이에요."),  # 실제 존재함 :contentReference[oaicite:4]{index=4}
        ],
        "락": [
            ("Counting Stars - OneRepublic", "리듬감 넘치고 희망적인 메시지를 담은 록송."),
            ("Smells Like Teen Spirit - Nirvana", "전설적인 록 사운드의 대표작."),
            ("Yellow - Coldplay", "사랑과 따뜻함을 담은 감성 록."),
            ("Boulevard of Broken Dreams - Green Day", "외로움 속에서도 자신을 찾는 노래."),
            ("Paradise - Coldplay", "현실의 벽을 넘어 꿈을 그리는 노래예요.")
        ],
        "R&B": [
            ("Peaches - Justin Bieber", "따뜻한 분위기의 R&B 대표곡."),
            ("Call Out My Name - The Weeknd", "아련한 감정을 세련되게 표현한 곡."),
            ("Get You - Daniel Caesar", "사랑에 빠진 순간을 그린 달콤한 노래."),
            ("Location - Khalid", "감정과 공간이 교차하는 독특한 분위기."),
            ("Under the Influence - Chris Brown", "몽환적인 분위기의 R&B 트랙.")
        ],
        "재즈": [
            ("Fly Me To The Moon - Frank Sinatra", "고전 재즈의 낭만을 느낄 수 있는 곡."),
            ("Take Five - Dave Brubeck", "재즈의 리듬을 대표하는 명곡이에요."),
            ("Autumn Leaves - Chet Baker", "가을 감성에 딱 어울리는 잔잔한 재즈."),
            ("Blue in Green - Miles Davis", "서정적인 감정선이 돋보이는 곡."),
            ("My Funny Valentine - Chet Baker", "부드럽고 감미로운 발렌타인데이의 정서.")
        ],
        "EDM": [
            ("Animals - Martin Garrix", "폭발적인 에너지의 EDM 대표곡."),
            ("Titanium - David Guetta", "자신감을 높여주는 강렬한 곡이에요."),
            ("Closer - The Chainsmokers", "로맨틱하면서도 신나는 EDM."),
            ("Wake Me Up - Avicii", "희망찬 감정을 담은 EDM 명곡."),
            ("Don't You Worry Child - Swedish House Mafia", "감동적인 멜로디가 인상적인 곡이에요.")
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

if st.button("💖 나만의 플레이리스트 만들어줘"):
    if not emotion.strip():
        st.warning("감정을 입력해주세요!")
    else:
        with st.spinner("너에게 어울리는 곡을 찾는 중... 🎶"):
            title, playlist = generate_playlist(emotion, weather, genre)

        cover_url = f"https://source.unsplash.com/800x600/?{emotion},{weather},{genre},pink,music,album"

        st.markdown(f"""
        <div style="text-align:center; margin-top:40px;">
            <img src="{cover_url}" width="75%" style="border-radius:25px; box-shadow:0 0 35px rgba(255,100,200,0.5);">
            <h2>{title}</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        for song in playlist:
            st.markdown(f"""
            <div class="playlist-card">
                <h4>{song['title']}</h4>
                <p style="color:#f8bbd0;">{song['desc']}</p>
                <a href="{song['url']}" target="_blank">🎧 YouTube에서 듣기</a>
            </div>
            """, unsafe_allow_html=True)

        st.balloons()
        st.success("💞 너만의 감성 플레이리스트가 완성됐어요!")

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("💖 2025 © 너를 위한 플레이리스트 | Designed with love by Yoojin 🎀")

# 하단
# ---------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("💿 2025 © 너를 위한 플레이리스트 | Designed by Yoojin 🎵")
