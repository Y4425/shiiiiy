import streamlit as st
st.title('김유진의 첫번째 앱ㅎㅎ')
st.subheader('하잉')
st.write('ㅎㅎㅎ')
st.write('https://www.youtube.com/channel/UCiZqWVAeChfqlom5ZPR3ZJA')
st.link_button('유튜브 바로가기', 'https://www.youtube.com/channel/UCiZqWVAeChfqlom5ZPR3ZJA')

name = st.text_input('이름을 입력해주세요 :')
if st.button('환영인사'):
    st.write(name+'님 안녕하세용')
    st.balloons()
    st.image('https://pbs.twimg.com/media/FyRM-GSaQAEmWgp.jpg')

st.success('성공')
st.warning('경고')
st.error('오류 ㅜㅜ')
st.info('안내문')
