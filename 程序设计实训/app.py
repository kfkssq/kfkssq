import streamlit as st

st.title("Hello Streamlit 🎈")
st.write("这是我的第一个 Streamlit App！")

number = st.slider("选择一个数字", 0, 100, 50)
st.write("你选择的是：", number)
